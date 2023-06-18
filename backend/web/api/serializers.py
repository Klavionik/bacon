from django.contrib.auth import get_user_model
from rest_framework import serializers

from web.products.models import Price, Product, Retailer, Store, UserProduct

User = get_user_model()


def validate_retailer_exists_for_url(url: str):
    try:
        Retailer.objects.get_by_product_url(url)
    except Retailer.DoesNotExist:
        raise serializers.ValidationError("No retailer for given URL.")


class ProductCreate(serializers.Serializer):
    url = serializers.URLField()

    class Meta:
        fields = ["url"]

    def validate_url(self, value: str):
        validate_retailer_exists_for_url(value)
        return value


class ProductPrice(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ["current", "old"]


class RetailerDetail(serializers.ModelSerializer):
    class Meta:
        model = Retailer
        fields = ["display_title", "id"]


class StoreDetail(serializers.ModelSerializer):
    retailer = RetailerDetail()

    class Meta:
        model = Store
        fields = ["retailer"]


class ProductDetail(serializers.ModelSerializer):
    price = ProductPrice(source="latest_price")
    store = StoreDetail()

    class Meta:
        model = Product
        fields = "__all__"


class UserProductCreate(serializers.ModelSerializer):
    product = ProductCreate()

    class Meta:
        model = UserProduct
        fields = ["product", "user"]

    def create(self, validated_data):
        user = validated_data["user"]
        product_url = validated_data["product"]["url"]

        retailer = Retailer.objects.get_by_product_url(product_url)
        store = retailer.get_user_store(user)
        product, _ = Product.objects.get_or_create(url=product_url, store=store)
        return UserProduct.objects.create(user=user, product=product)


class UserProductList(serializers.ModelSerializer):
    product = ProductDetail()

    class Meta:
        model = UserProduct
        exclude = ["user"]


class UserProductDestroy(serializers.ModelSerializer):
    class Meta:
        fields = ["id"]
