import sys

import loguru

logger_configured = False


def configure_logger(enable_backtrace: bool = False, enable_disagnose: bool = False):
    global logger_configured

    if logger_configured:
        return

    loguru.logger.remove(0)
    loguru.logger.add(
        sys.stderr,
        level="INFO",
        format="<g>[{time:DD.MM.YYYY HH:mm:ss}]</> <lvl>{level: <8}</> | <lvl>{message}</>",
        backtrace=enable_backtrace,
        diagnose=enable_disagnose,
    )
    logger_configured = True
