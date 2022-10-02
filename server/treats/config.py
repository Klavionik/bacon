from pydantic import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    ROOT_DIR = Path(__file__).parent.parent
    DEBUG: int
    BOT_TOKEN: str
    TELEGRAM_BASE_URL: str
    SERVER_URL: str
    SERVER_SECRET: str
    WHITELIST: list

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


settings = Settings()
