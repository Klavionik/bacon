from pydantic import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    ROOT_DIR: Path = Path(__file__).parent
    DEBUG: int = 0
    PEREKRESTOK_API_URL: str = 'https://www.perekrestok.ru/api/customer/1.4.1.0'
    TELEGRAM_BASE_URL: str = 'https://api.telegram.org/bot%(token)s'

    HOST: str
    TUNNEL_URL: str = ""
    SERVER_SECRET: str
    DB_URI: str
    CORS_ALLOWED_ORIGIN: list

    BOT_TOKEN: str
    LOGTAIL_TOKEN: str = ""
    SENTRY_DSN: str = ""

    @property
    def server_url(self):
        if self.DEBUG:
            return self.TUNNEL_URL
        return self.HOST


settings = Settings()
