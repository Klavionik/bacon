from dataclasses import dataclass
from typing import Optional

from django.contrib.auth import get_user_model
from django.db import models, transaction
from django.db.models import OuterRef, Subquery, functions
from loguru import logger

from web.scraping.models import Scraper, ScraperDisabled
from web.scraping.providers.models import ProductData

User = get_user_model()


class ProductFetchError(Exception):
    pass


@dataclass
class ProductUpdate:
    product_id: int
    product_title: str

    availability_before: bool
    price_before: float
    old_price_before: float | None

    availability_after: bool | None = None
    price_after: float | None = None
    old_price_after: float | None = None

    @property
    def availability_changed(self):
        return self.availability_after != self.availability_before

    @property
    def price_changed(self):
        return self.price_after != self.price_before

    @property
    def product_changed(self):
        return self.availability_changed or self.price_changed


class RetailerQuerySet(models.QuerySet):
    def scrapable(self):
        return self.filter(scraper__enabled=True)


class RetailerManager(models.Manager):
    def get_by_product_url(self, url: str):
        return self.get(product_url_pattern__reverse_regex=url)


class ProductManager(models.Manager):
    def with_latest_price(self):
        subquery_qs = (
            Price.objects.filter(product=OuterRef("id"))
            .only("current", "old")
            .order_by("-created_at")
            .values(
                price=functions.JSONObject(
                    current="current",
                    old="old",
                )
            )
        )[:1]
        latest_price_subquery = Subquery(product=OuterRef("pk"), queryset=subquery_qs)
        return self.annotate(latest_price=latest_price_subquery)


class UserProductQuerySet(models.QuerySet):
    def filter_by_user(self, user: User):
        return self.filter(user=user)


class UserProductManager(models.Manager):
    def get_queryset(self):
        return UserProductQuerySet(self.model, using=self._db)

    def from_product_url(self, user: User, url: str):
        retailer = Retailer.objects.get_by_product_url(url)
        store = retailer.get_user_store(user)
        product, _ = Product.objects.get_or_create(url=url, store=store)
        return self.create(user=user, product=product)


class UserStoreQuerySet(models.QuerySet):
    def filter_by_user(self, user: User):
        return self.filter(user=user)


class ReverseRegex(models.Lookup):
    """
    Reverse regex search compatible with PostgreSQL query syntax.

    The same as:

    SELECT *
    FROM table
    WHERE 'value' ~ table.pattern;
    """

    lookup_name = "reverse_regex"

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        return "%s ~ %s" % (rhs, lhs), params


models.CharField.register_class_lookup(ReverseRegex)


class Retailer(models.Model):
    title = models.CharField(max_length=64, unique=True)
    display_title = models.CharField(max_length=64)
    product_url_pattern = models.CharField(max_length=128, unique=True)
    scraper = models.OneToOneField(Scraper, on_delete=models.PROTECT)

    objects = RetailerManager.from_queryset(RetailerQuerySet)()

    def __str__(self):
        return self.display_title

    def get_user_store(self, user: User):
        return user.stores.filter(retailer=self).first()

    def fetch_products(self, urls: str | list[str], store_id: str):
        return self.scraper.fetch_products(urls, store_id)

    def search_stores(self, search_term: str):
        return self.scraper.fetch_stores(search_term)

    def update_products(self) -> list[ProductUpdate]:
        product_updates = []

        for store in self.stores.all():
            for product in store.products.iterator(chunk_size=2000):
                product: Product
                product_update = product.update()

                if product_update:
                    product_updates.append(product_update)

        return product_updates


class Store(models.Model):
    title = models.CharField(max_length=128)
    address = models.CharField(max_length=128)
    external_id = models.CharField(max_length=128)
    retailer = models.ForeignKey(Retailer, related_name="stores", on_delete=models.CASCADE)

    class Meta:
        constraints = [models.UniqueConstraint("retailer", "external_id", name="uniq_retailer")]

    def __str__(self):
        return self.title

    def fetch_products(self, urls: str | list[str]):
        return self.retailer.fetch_products(urls, self.external_id)


class Product(models.Model):
    class ProcessingStatus(models.TextChoices):
        PENDING = "pending"
        DONE = "done"
        ERROR = "error"

    title = models.CharField(max_length=256, blank=True)
    url = models.URLField(unique=True)
    in_stock = models.BooleanField(null=True)
    meta = models.JSONField(default=dict, blank=True)
    store = models.ForeignKey(Store, related_name="products", on_delete=models.RESTRICT)
    processing_status = models.CharField(
        max_length=32,
        default=ProcessingStatus.PENDING,
        choices=ProcessingStatus.choices,
    )

    objects = ProductManager()

    def __str__(self):
        return self.url

    @transaction.atomic
    def ingest(self) -> None:
        logger.info(f"Try to ingest product {self.url}.")

        if self.processing_status != self.ProcessingStatus.PENDING:
            logger.warning("Product was already ingested.")
            return

        try:
            data = self._fetch_product_data()
        except ProductFetchError:
            self.processing_status = self.ProcessingStatus.ERROR
            self.save(update_fields=["processing_status"])
            return

        self.title = data.title
        self.meta = data.metadata
        self.in_stock = data.available
        self.add_price(data.price, data.old_price)

        self.processing_status = self.ProcessingStatus.DONE
        self.save(update_fields=["title", "in_stock", "meta", "processing_status"])

        logger.info("Ingest finished.")

    @transaction.atomic
    def update(self) -> ProductUpdate | None:
        logger.info(f"Try to update product {self.url}.")

        if self.processing_status != self.ProcessingStatus.DONE:
            logger.warning("Won't update, ingest is not done yet.")
            return

        price = self.get_latest_price()
        update = ProductUpdate(
            product_id=self.id,
            product_title=self.title,
            availability_before=self.in_stock,
            price_before=price.current,
            old_price_before=price.old,
        )
        try:
            data = self._fetch_product_data()
        except ProductFetchError:
            logger.warning("Cannot update product.")
            return

        self.title = data.title
        self.meta = data.metadata

        if self.in_stock != data.available:
            logger.info(f"Availability changed: {self.in_stock} -> {data.available}.")
            self.in_stock = data.available

        if price.current != data.price:
            logger.info(f"Price changed: {price.current} -> {data.price}.")
            self.add_price(data.price, data.old_price)

        self.save(update_fields=["title", "in_stock", "meta"])
        logger.info("Update complete.")

        update.availability_after = data.available
        update.price_after = data.price
        update.old_price_after = data.old_price

        return update

    def add_price(self, current: float, old: float | None) -> None:
        Price.objects.create(current=current, old=old, product=self)

    def get_latest_price(self) -> Optional["Price"]:
        try:
            return self.prices.latest("created_at")
        except Price.DoesNotExist:
            pass

    def _fetch_product_data(self) -> ProductData | None:
        try:
            return self.store.fetch_products(self.url)
        except ScraperDisabled:
            logger.info(f"Abort fetching {self.url}: retailer {self.store.retailer} is disabled.")
            return
        except Exception as exc:
            logger.error(f"Error while fetching product {self.url}. Reason: {exc}.")
            raise ProductFetchError


class Price(models.Model):
    current = models.FloatField()
    old = models.FloatField(null=True, blank=True)
    product = models.ForeignKey(Product, related_name="prices", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.current)


class UserProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    objects = UserProductManager.from_queryset(UserProductQuerySet)()

    class Meta:
        constraints = [models.UniqueConstraint("user", "product", name="uniq_user_product")]


class UserStore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    objects = UserStoreQuerySet.as_manager()

    class Meta:
        constraints = [models.UniqueConstraint("user", "store", name="uniq_user_store")]
