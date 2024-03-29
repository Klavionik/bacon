from django.db.models.signals import post_save
from django.dispatch import receiver

from web.products.models import Product


@receiver(post_save, sender=Product)
def ingest_product(sender, instance: Product, created: bool, **_kwargs):
    if not created:
        return

    instance.ingest()
