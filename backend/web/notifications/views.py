from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.views import APIView, Response

from web.notifications import telegram
from web.notifications.models import TelegramSubscription

User = get_user_model()


class GetDeepLinkAPIView(APIView):
    def get(self, request, *args, **kwargs):
        return Response(data={"link": telegram.make_deep_link(self.request.user)})


class HandleTelegramUpdate(APIView):
    def post(self, request, *args, **kwargs):
        client = telegram.get_client()
        update = telegram.Update.from_json(self.request.data)

        if update.is_deep_link:
            user_data = telegram.decode_deep_link_token(update.deep_link_token)
            user_id = int(user_data.split(":")[1])

            if TelegramSubscription.objects.filter(user_id=user_id).exists():
                msg = "Вы уже подписались на уведомления."
                client.send_message(update.message.chat.id, msg)
                return Response()

            TelegramSubscription.objects.create(user_id=user_id, chat_id=update.message.chat.id)
            msg = "Вы успешно подписались на уведомления."
            client.send_message(update.message.chat.id, msg)
            return Response()

        msg = "Привет! Чтобы использовать этого бота, нужно подписаться в Настройках."
        client.send_message(update.message.chat.id, msg)
        return Response()


class TelegramSubscriptionAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            self.request.user.telegram_subscription
        except User.telegram_subscription.RelatedObjectDoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response()

    def delete(self, request, *args, **kwargs):
        try:
            self.request.user.telegram_subscription.delete()
        except User.telegram_subscription.RelatedObjectDoesNotExist:
            pass

        return Response(status=status.HTTP_204_NO_CONTENT)
