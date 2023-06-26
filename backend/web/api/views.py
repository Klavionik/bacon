from django.db.models import Prefetch
from rest_framework import exceptions, permissions
from rest_framework.generics import (
    DestroyAPIView,
    GenericAPIView,
    ListAPIView,
    ListCreateAPIView,
)
from rest_framework.response import Response

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


class RetailerList(ListAPIView):
    queryset = products_models.Retailer.objects.all()
    serializer_class = serializers.RetailerDetail
    permission_classes = [permissions.IsAuthenticated]


class UserStoreListCreate(ListCreateAPIView):
    serializer_class = serializers.UserStoreListCreate
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return products_models.UserStore.objects.filter_by_user(self.request.user)


class RetailerStoreSearch(GenericAPIView):
    queryset = products_models.Retailer.objects.select_related("scraper")

    def get(self, request, *args, **kwargs):
        retailer = self.get_object()
        search_term = self.request.query_params.get("term")

        if search_term is None:
            raise exceptions.ValidationError("Missing required query param 'term'.")

        stores = retailer.search_stores(search_term)
        serializer = serializers.StoreSuggestion(stores, many=True)
        return Response(data=serializer.data)
