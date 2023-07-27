from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class TelegramSubscription(models.Model):
    chat_id = models.IntegerField()
    user = models.OneToOneField(
        User, related_name="telegram_subscription", on_delete=models.CASCADE
    )
