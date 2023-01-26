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
    CORS_ALLOWED_ORIGIN: list = []
    PROXY: str | None = None

    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    CACHE_QUEUE_DB: int = 1

    BOT_TOKEN: str
    LOGTAIL_TOKEN: str = ""
    SENTRY_DSN: str = ""

    @property
    def server_url(self):
        if self.DEBUG:
            return self.TUNNEL_URL
        return self.HOST

    @property
    def db_uri(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@db/{self.DB_NAME}"

    @property
    def queue_uri(self):
        return f"redis://cache/{self.CACHE_QUEUE_DB}"


settings = Settings()
