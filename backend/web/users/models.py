from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    products = models.ManyToManyField("products.Product", through="products.UserProduct")
    stores = models.ManyToManyField("products.Store", through="products.UserStore")
