from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "web.api"

    def ready(self):
        super().ready()

        from web.api import receivers  # noqa
