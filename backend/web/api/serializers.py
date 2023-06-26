from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers, status

from web.products.models import Price, Product, Retailer, Store, UserProduct, UserStore

User = get_user_model()


def validate_retailer_exists_for_url(url: str):
    try:
        Retailer.objects.get_by_product_url(url)
    except Retailer.DoesNotExist:
        raise serializers.ValidationError("No retailer for given URL.")


def validate_userstore_exists_for_retailer(url: str, user: User):
    retailer = Retailer.objects.get_by_product_url(url)
    store = retailer.get_user_store(user)

    if store is None:
        raise serializers.ValidationError(f"User has no store for retailer {retailer.title}.")


def validate_unique_product_user(product_url: str, user: User):
    if UserProduct.objects.filter(product__url=product_url, user=user).exists():
        raise Conflict("Fields product, user must make a unique set.")


def validate_unique_store_user(store: Store, user: User):
    if UserStore.objects.filter(store=store, user=user).exists():
        raise Conflict("Fields store, user must make a unique set.")


class Conflict(serializers.ValidationError):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Impossible action."
    default_code = "conflict"


class ProductPrice(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ["current", "old"]


class RetailerDetail(serializers.ModelSerializer):
    class Meta:
        model = Retailer
        exclude = ["scraper"]


class StoreDetail(serializers.ModelSerializer):
    retailer = RetailerDetail()

    class Meta:
        model = Store
        fields = "__all__"


class ProductCreate(serializers.ModelSerializer):
    url = serializers.URLField()
    price = serializers.SerializerMethodField()
    store = StoreDetail(read_only=True)

    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ["title", "in_stock", "store", "processing_status", "price", "meta"]

    def validate_url(self, value: str):
        validate_retailer_exists_for_url(value)
        validate_userstore_exists_for_retailer(value, self.context["request"].user)
        return value

    def get_price(self, product: Product):
        try:
            price = product.prices.latest("-created_at")
        except Price.DoesNotExist:
            return None

        return ProductPrice(instance=price).data


class ProductDetail(serializers.ModelSerializer):
    price = ProductPrice(source="latest_price")
    store = StoreDetail()

    class Meta:
        model = Product
        exclude = ["meta"]


class UserProductCreate(serializers.ModelSerializer):
    product = ProductCreate()

    class Meta:
        model = UserProduct
        fields = ["product", "id"]

    def create(self, validated_data):
        user = self.context["request"].user
        product_url = validated_data["product"]["url"]

        # Validate here to return a 409 in case of error, not 400.
        validate_unique_product_user(product_url, user)
        return UserProduct.objects.from_product_url(user, product_url)


class UserProductList(serializers.ModelSerializer):
    product = ProductDetail()

    class Meta:
        model = UserProduct
        fields = ["product", "id"]


class StoreCreate(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = "__all__"


class UserStoreListCreate(serializers.ModelSerializer):
    store = StoreCreate()

    class Meta:
        model = UserStore
        exclude = ["user"]

    def create(self, validated_data):
        user = self.context["request"].user
        store_qs = Store.objects.select_for_update()

        with transaction.atomic():
            store, _ = store_qs.get_or_create(
                external_id=validated_data["store"]["external_id"],
                retailer=validated_data["store"]["retailer"],
                defaults=validated_data["store"],
            )

        # Validate here to return a 409 in case of error, not 400.
        validate_unique_store_user(store, user)
        return UserStore.objects.create(user=user, store=store)


class StoreSuggestion(serializers.Serializer):
    title = serializers.CharField()
    address = serializers.CharField()
    external_id = serializers.IntegerField(source="id")
