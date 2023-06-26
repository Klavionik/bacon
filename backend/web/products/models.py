from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import OuterRef, Subquery, functions
from loguru import logger

from web.scraping.models import Scraper, ScraperDisabled

User = get_user_model()


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

    objects = RetailerManager()

    def __str__(self):
        return self.display_title

    def get_user_store(self, user: User):
        return user.stores.filter(retailer=self).first()

    def fetch_products(self, urls: str | list[str], store_id: str):
        return self.scraper.fetch_products(urls, store_id)

    def search_stores(self, search_term: str):
        return self.scraper.fetch_stores(search_term)


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

    def update(self) -> bool:
        logger.info(f"Updating product {self.url}.")

        try:
            data = self.store.fetch_products(self.url)
        except ScraperDisabled:
            logger.info(f"Abort fetching {self.url}: retailer {self.store.retailer} is disabled.")
            return False
        except Exception as exc:
            self.processing_status = self.ProcessingStatus.ERROR
            self.save(update_fields=["processing_status"])
            logger.error(f"Error while updating product {self.url}. Reason: {exc}.")
            return False

        self.title = data.title
        self.meta = data.metadata

        if self.in_stock != data.available:
            logger.info(
                f"Availability changed for product {self.url}: {self.in_stock} -> {data.available}."
            )
            self.in_stock = data.available

        try:
            latest_price = self.prices.latest("-created_at")
            if latest_price.current != data.price:
                logger.info(
                    f"Price changed for product {self.url}: {latest_price.current} -> {data.price}."
                )
                self.add_price(data.price, data.old_price)
        except Price.DoesNotExist:
            logger.info(f"Price added for product {self.url}.")
            self.add_price(data.price, data.old_price)

        self.save(update_fields=["title", "in_stock", "meta"])
        logger.info(f"Product {self.url} update complete.")

        self.finish_processing()
        return True

    def finish_processing(self):
        if self.processing_status != self.ProcessingStatus.PENDING:
            return

        self.processing_status = self.ProcessingStatus.DONE
        self.save(update_fields=["processing_status"])

    def add_price(self, current: float, old: float | None):
        Price.objects.create(current=current, old=old, product=self)


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
