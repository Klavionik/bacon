from django.db.models import Prefetch
from rest_framework import permissions
from rest_framework.generics import DestroyAPIView, ListCreateAPIView

from web.api import serializers
from web.products import models as products_models


class UserProductListCreate(ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return serializers.UserProductCreate
        return serializers.UserProductList

    def get_queryset(self):
        product_qs = products_models.Product.objects.with_latest_price()
        userproduct_qs = products_models.UserProduct.objects.prefetch_related(
            Prefetch("product", product_qs)
        )
        return userproduct_qs.filter_by_user(self.request.user)


class UserProductDestroy(DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return products_models.UserProduct.objects.filter_by_user(self.request.user)
