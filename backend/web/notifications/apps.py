from django.apps import AppConfig

from web.notifications import telegram


class NotificationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "web.notifications"

    def ready(self):
        super().ready()
        from web.notifications import receivers  # noqa

        telegram.initialize_webhook(telegram.get_client())
