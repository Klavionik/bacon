from django.db import models


class RetailerManager(models.Manager):
    def get_by_product_url(self, url: str):
        return self.get(product_url_pattern__reverse_regex=url)
