from django.conf import settings
from django.db import models
from django.utils.module_loading import import_string

from scrapers.base import BaseScraper
from web.scraping.utils import list_scrapers


def get_scrapers_choices():
    scrapers = list_scrapers(settings.SCRAPERS_DIR)
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
    def _instance(self) -> BaseScraper:
        class_ = import_string(self.entrypoint)
        return class_(**self.config)

    def fetch(self, url: str, store_id: str):
        if not self.enabled:
            raise ScraperDisabled(f"Scraper {self} is disabled.")

        return self._instance.fetch(url, store_id)
