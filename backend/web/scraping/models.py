from django.conf import settings
from django.db import models
from django.utils.module_loading import import_string

from web.scraping.utils import list_scrapers


def get_scrapers_choices():
    scrapers = list_scrapers(settings.SCRAPERS_DIR)
    return list(zip(scrapers, scrapers))


class Scraper(models.Model):
    entrypoint = models.CharField(max_length=256, choices=get_scrapers_choices())
    config = models.JSONField(blank=True, default=dict)

    @property
    def instance(self):
        class_ = import_string(self.entrypoint)
        return class_(**self.config)
