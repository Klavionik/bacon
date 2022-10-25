import loguru
import sentry_sdk
import logtail
import sys
from config import settings

logger_configured = False
sentry_configured = False


def configure_logger():
    global logger_configured

    if logger_configured:
        return

    logger_configured = True

    loguru.logger.remove(0)
    loguru.logger.add(
        sys.stderr,
        level='INFO',
        format='<g>[{time:DD.MM.YYYY HH:mm:ss}]</> <lvl>{level: <8}</> | <lvl>{message}</>',
        backtrace=settings.DEBUG,
        diagnose=settings.DEBUG,
    )

    if not settings.DEBUG:
        handler = logtail.LogtailHandler(settings.LOGTAIL_TOKEN, raise_exceptions=True)
        loguru.logger.add(
            handler,
            format='{message}',
            level='INFO',
            backtrace=False,
            diagnose=False,
        )


def configure_sentry() -> None:
    global sentry_configured

    if not settings.DEBUG or sentry_configured:
        return

    sentry_configured = True

    sentry_sdk.init(
        settings.SENTRY_DSN,
        traces_sample_rate=0.5,
    )
