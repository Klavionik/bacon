from cuser.models import AbstractCUser
from django.db import models


class User(AbstractCUser):
    products = models.ManyToManyField("products.Product", through="products.UserProduct")
    stores = models.ManyToManyField("products.Store", through="products.UserStore")
