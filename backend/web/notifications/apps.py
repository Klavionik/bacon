from django.apps import AppConfig
from django.conf import settings
from loguru import logger

from web.notifications import telegram


class NotificationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "web.notifications"

    def ready(self):
        super().ready()
        from web.notifications import receivers  # noqa

        if not settings.CI:
            try:
                telegram.initialize_webhook(telegram.get_client())
            except telegram.TelegramAPIError as exc:
                logger.warning(f"Could not initialize webhook due to error: {exc}.")
