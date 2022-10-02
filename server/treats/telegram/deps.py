from functools import lru_cache

from config import settings
from telegram.client import TelegramClient


@lru_cache
def get_telegram_client():
    return TelegramClient(
        base_url=settings.TELEGRAM_BASE_URL,
        token=settings.BOT_TOKEN,
        server_url=settings.SERVER_URL,
        server_secret=settings.SERVER_SECRET,
    )
