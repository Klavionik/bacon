from typing import Iterable

from django.conf import settings
from django.db import models
from django.utils.module_loading import import_string

from web.scraping.providers.base import BaseProvider
from web.scraping.providers.models import ProductData, Store
from web.scraping.utils import list_scrapers


def get_scrapers_choices():
    scrapers = list_scrapers(settings.PROVIDERS_MODULE)
    return list(zip(scrapers, scrapers))


class ScraperDisabled(RuntimeError):
    pass


class Scraper(models.Model):
    entrypoint = models.CharField(max_length=256, choices=get_scrapers_choices())
    config = models.JSONField(blank=True, default=dict)
    enabled = models.BooleanField(default=False)

    def __str__(self):
        return self.entrypoint.split(".")[-1]

    @property
    def _instance(self) -> BaseProvider:
        class_ = import_string(self.entrypoint)
        return class_(**self.config)

    def fetch_products(
        self, urls: str | list[str], store_id: str
    ) -> ProductData | Iterable[ProductData]:
        if not self.enabled:
            raise ScraperDisabled(f"Scraper {self} is disabled.")

        return self._instance.fetch_products(urls, store_id)

    def fetch_stores(self, address: str) -> Iterable[Store]:
        return self._instance.fetch_stores(address)
