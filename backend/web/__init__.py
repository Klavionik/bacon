from django.conf import settings

from logger import configure_logger
from web.celery import app as celery_app
from web.sentry import initialize_sentry

initialize_sentry()
configure_logger(enable_backtrace=settings.DEBUG, enable_disagnose=settings.DEBUG)

__all__ = ["celery_app"]
