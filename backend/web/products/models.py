from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


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


class Store(models.Model):
    title = models.CharField(max_length=128)
    address = models.CharField(max_length=128)
    external_id = models.CharField(max_length=128)
    retailer = models.ForeignKey(Retailer, related_name="stores", on_delete=models.CASCADE)

    class Meta:
        constraints = [models.UniqueConstraint("retailer", "external_id", name="uniq_retailer")]


class Product(models.Model):
    title = models.CharField(max_length=256)
    url = models.URLField(unique=True)
    available = models.BooleanField(default=True)
    meta = models.JSONField(default=dict, blank=True)
    store = models.ForeignKey(Store, related_name="products", on_delete=models.RESTRICT)


class Price(models.Model):
    value = models.FloatField()
    product = models.ForeignKey(Product, related_name="prices", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class UserProduct(models.Model):
    user = models.ForeignKey(User, related_name="products", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="users", on_delete=models.CASCADE)

    class Meta:
        constraints = [models.UniqueConstraint("user", "product", name="uniq_user_product")]


class UserStore(models.Model):
    user = models.ForeignKey(User, related_name="stores", on_delete=models.CASCADE)
    store = models.ForeignKey(Store, related_name="+", on_delete=models.CASCADE)

    class Meta:
        constraints = [models.UniqueConstraint("user", "store", name="uniq_user_store")]