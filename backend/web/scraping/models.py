import tomli
import tomli_w
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.module_loading import import_string

from web.products.models import Retailer
from web.scraping.utils import list_scrapers


def get_scrapers_choices():
    scrapers = list_scrapers(settings.SCRAPERS_DIR)
    return list(zip(scrapers, scrapers))


class TOMLField(models.TextField):
    description = "A TOML-compliant text field."

    def get_prep_value(self, value):
        return tomli_w.dumps(value)

    def value_from_object(self, obj):
        value = super().value_from_object(obj)
        return tomli_w.dumps(value)

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value

        try:
            return tomli.loads(value)
        except tomli.TOMLDecodeError:
            raise ValidationError("Value must be valid TOML.")


class Scraper(models.Model):
    entrypoint = models.CharField(max_length=256, choices=get_scrapers_choices())
    config = TOMLField(blank=True)
    retailer = models.OneToOneField(Retailer, on_delete=models.CASCADE)

    @property
    def instance(self):
        class_ = import_string(self.entrypoint)
        return class_(**self.config)
