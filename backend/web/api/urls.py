from django.urls import path

from web.api.views import RetailerList, UserProductDestroy, UserProductListCreate

urlpatterns = [
    path("userproducts/", UserProductListCreate.as_view()),
    path("userproducts/<int:pk>/", UserProductDestroy.as_view()),
    path("retailers/", RetailerList.as_view()),
]
