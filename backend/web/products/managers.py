from django.db import models
from django.db.models import OuterRef, Subquery, functions


class RetailerManager(models.Manager):
    def get_by_product_url(self, url: str):
        return self.get(product_url_pattern__reverse_regex=url)


class ProductManager(models.Manager):
    def with_latest_price(self):
        subquery_qs = (
            self.model.prices.field.model.objects.filter(product=OuterRef("id"))
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
