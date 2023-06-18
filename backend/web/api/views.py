from django.db.models import Prefetch
from rest_framework.generics import DestroyAPIView, ListCreateAPIView

from web.api import serializers
from web.products import models as products_models


class UserProductListCreate(ListCreateAPIView):
    queryset = products_models.UserProduct.objects.all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return serializers.UserProductCreate
        return serializers.UserProductList

    def get_queryset(self):
        if self.request.method == "POST":
            return super().get_queryset()

        product_qs = products_models.Product.objects.with_latest_price()
        return products_models.UserProduct.objects.prefetch_related(Prefetch("product", product_qs))


class UserProductDestroy(DestroyAPIView):
    queryset = products_models.UserProduct.objects.all()
    serializer_class = serializers.UserProductDestroy
