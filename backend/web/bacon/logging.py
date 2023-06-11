import sys

import loguru
from django.conf import settings

logger_configured = False


def configure_logger():
    global logger_configured

    if logger_configured:
        return

    loguru.logger.remove(0)
    loguru.logger.add(
        sys.stderr,
        level="INFO",
        format="<g>[{time:DD.MM.YYYY HH:mm:ss}]</> <lvl>{level: <8}</> | <lvl>{message}</>",
        backtrace=settings.DEBUG,
        diagnose=settings.DEBUG,
    )
    logger_configured = True
