from django.apps import AppConfig


class ProductsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "web.products"

    def ready(self):
        super().ready()

        from web.products import receivers  # noqa
