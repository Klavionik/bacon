from pydantic import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str
    BASE_URL: str
    SERVER_URL: str
    SERVER_SECRET: str
    WHITELIST: list

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DB_HOST: str
    DB_URI: str

    class Config:
        env_file = '.env'


settings = Settings()
