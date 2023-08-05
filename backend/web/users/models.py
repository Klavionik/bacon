from cuser.models import AbstractCUser, CUserManager
from django.contrib.postgres import aggregates
from django.db import models


class UserQuerySet(models.QuerySet):
    def notifiable(self):
        return self.filter(telegram_subscription__isnull=False)

    def with_products_ids(self):
        return self.annotate(products_ids=aggregates.ArrayAgg("userproduct__product_id"))


class User(AbstractCUser):
    products = models.ManyToManyField("products.Product", through="products.UserProduct")
    stores = models.ManyToManyField("products.Store", through="products.UserStore")

    objects = CUserManager.from_queryset(UserQuerySet)()

    def send_products_update_notification(self, notification):
        return self.telegram_subscription.send_message(notification, html=True)
