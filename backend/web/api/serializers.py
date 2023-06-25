from django.contrib.auth import get_user_model
from rest_framework import serializers, status

from web.products.models import Price, Product, Retailer, Store, UserProduct

User = get_user_model()


def validate_retailer_exists_for_url(url: str):
    try:
        Retailer.objects.get_by_product_url(url)
    except Retailer.DoesNotExist:
        raise serializers.ValidationError("No retailer for given URL.")


def validate_unique_product_user(product_url: str, user: User):
    if UserProduct.objects.filter(product__url=product_url, user=user).exists():
        raise Conflict("Fields product, user must make a unique set.")


class Conflict(serializers.ValidationError):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Impossible action."
    default_code = "conflict"


class ProductCreate(serializers.ModelSerializer):
    url = serializers.URLField()

    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ["title", "in_stock", ""]
        exclude = ["store"]

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
        fields = ["product"]

    def create(self, validated_data):
        user = self.context["request"].user
        product_url = validated_data["product"]["url"]

        # Validate here to return a 409 in case of error, not 400.
        validate_unique_product_user(product_url, user)
        return UserProduct.objects.from_product_url(user, product_url)


class UserProductList(serializers.ModelSerializer):
    product = ProductDetail()
    user = serializers.SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = UserProduct
        fields = ["product", "user"]


class UserProductDestroy(serializers.ModelSerializer):
    class Meta:
        fields = ["id"]
