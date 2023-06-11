import sentry_sdk
from django.conf import settings
from sentry_sdk.integrations.django import DjangoIntegration

initialized = False


def initialize_sentry():
    global initialized

    if settings.DEBUG:
        return

    if initialized:
        return

    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        integrations=[DjangoIntegration()],
        traces_sample_rate=0.5,
    )
    initialized = True
