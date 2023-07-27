from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

from web.notifications import models, telegram


@receiver(pre_delete, sender=models.TelegramSubscription)
def send_unsubscribed_message(sender, instance: models.TelegramSubscription, *args, **kwargs):
    client = telegram.get_client()
    msg = "Вы отказались от получения уведомлений."
    client.send_message(instance.chat_id, msg)
