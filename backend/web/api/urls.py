from django.urls import path

from web.api.views import (
    RetailerList,
    RetailerStoreSearch,
    UserProductDestroy,
    UserProductListCreate,
    UserStoreDestroy,
    UserStoreListCreate,
)

urlpatterns = [
    path("userproducts/", UserProductListCreate.as_view()),
    path("userproducts/<int:pk>/", UserProductDestroy.as_view()),
    path("retailers/", RetailerList.as_view()),
    path("retailers/<int:pk>/stores/search/", RetailerStoreSearch.as_view()),
    path("userstores/", UserStoreListCreate.as_view()),
    path("userstores/<int:pk>/", UserStoreDestroy.as_view()),
]
