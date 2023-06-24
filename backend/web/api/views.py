from django.db.models import Prefetch
from rest_framework import permissions
from rest_framework.generics import DestroyAPIView, ListCreateAPIView

from web.api import filters, serializers
from web.products import models as products_models


class UserProductListCreate(ListCreateAPIView):
    queryset = products_models.UserProduct.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = filters.UserProductFilter

    def get_serializer_class(self):
        if self.request.method == "POST":
            return serializers.UserProductCreate
        return serializers.UserProductList

    def get_queryset(self):
        if self.request.method == "POST":
            return super().get_queryset()

        product_qs = products_models.Product.objects.with_latest_price()
        userproduct_qs = products_models.UserProduct.objects.prefetch_related(
            Prefetch("product", product_qs)
        )
        username = self.request.query_params.get("username")

        if not username:
            userproduct_qs = userproduct_qs.filter_by_user(self.request.user)

        return userproduct_qs


class UserProductDestroy(DestroyAPIView):
    queryset = products_models.UserProduct.objects.all()
    serializer_class = serializers.UserProductDestroy
