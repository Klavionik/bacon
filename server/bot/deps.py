from functools import lru_cache
from core.clients import TelegramClient

from ..settings import settings


@lru_cache
def get_telegram_client():
    return TelegramClient(
        base_url=settings.BASE_URL,
        token=settings.BOT_TOKEN,
        server_url=settings.SERVER_URL,
        server_secret=settings.SERVER_SECRET,
    )
