from django.contrib.auth import get_user_model
from django.db import models

from web.notifications.telegram import get_client

User = get_user_model()


class TelegramSubscription(models.Model):
    chat_id = models.IntegerField()
    user = models.OneToOneField(
        User, related_name="telegram_subscription", on_delete=models.CASCADE
    )

    def send_message(self, message: str, *, html: bool = False) -> dict:
        client = get_client()
        return client.send_message(self.chat_id, message, html=html)
