from django.urls import path

from web.notifications import views

urlpatterns = [
    path("telegram/update/", views.HandleTelegramUpdate.as_view(), name="telegram_update"),
    path("telegram/deep_link/", views.GetDeepLinkAPIView.as_view(), name="get_deep_link"),
    path("telegram/subscription/", views.TelegramSubscriptionAPIView.as_view()),
]
