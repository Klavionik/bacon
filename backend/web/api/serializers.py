from django.contrib.auth import get_user_model
from rest_framework import serializers

from web.products import models as products_models

User = get_user_model()


class ProductCreate(serializers.ModelSerializer):
    class Meta:
        model = products_models.Product
        fields = ["url"]


class ProductPrice(serializers.ModelSerializer):
    class Meta:
        model = products_models.Price
        fields = ["current", "old"]


class ProductDetail(serializers.ModelSerializer):
    price = ProductPrice(source="latest_price")

    class Meta:
        model = products_models.Product
        fields = "__all__"


class UserProductCreate(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    product = serializers.SlugRelatedField(
        queryset=products_models.Product.objects.all(), slug_field="url"
    )

    class Meta:
        model = products_models.UserProduct
        fields = ["user", "product"]


class UserProductList(serializers.ModelSerializer):
    product = ProductDetail()

    class Meta:
        model = products_models.UserProduct
        exclude = ["user"]


class UserProductDestroy(serializers.ModelSerializer):
    class Meta:
        fields = ["id"]
