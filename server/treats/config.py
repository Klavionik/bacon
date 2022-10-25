from pydantic import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    ROOT_DIR = Path(__file__).parent.parent
    DEBUG: int
    BOT_TOKEN: str
    PEREKRESTOK_API_URL: str
    TELEGRAM_BASE_URL: str
    SERVER_URL: str
    SERVER_SECRET: str
    AUTH0_DOMAIN: str
    AUTH0_AUDIENCE: str
    AUTH0_ID: str
    AUTH0_SECRET: str
    ALLOWED_USERS: list
    CORS_ALLOWED_ORIGIN: list
    SENTRY_DSN: str
    LOGTAIL_TOKEN: str

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DB_HOST: str

    class Config:
        env_file = '.env'

    @property
    def db_uri(self):
        if self.DEBUG:
            path = self.ROOT_DIR / 'db.sqlite3'
            return f'sqlite+aiosqlite:///{path}'
        return f'postgres://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.DB_HOST}/{self.POSTGRES_DB}'

    @property
    def auth0_jwks_url(self):
        return f'https://{self.AUTH0_DOMAIN}/.well-known/jwks.json'

    @property
    def auth0_issuer(self):
        return f'https://{self.AUTH0_DOMAIN}/'

    @property
    def auth0_api_url(self):
        return f'https://{self.AUTH0_DOMAIN}/api/v2/'


settings = Settings()
