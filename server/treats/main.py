from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from api.routes import router as api_router
from storage import create_db_engine
from telegram.deps import get_telegram_client
from telegram.routes import router as bot_router
from config import settings


def setup_event_handlers(app):
    @app.on_event('startup')
    async def on_startup():
        client = get_telegram_client()
        webhook_info = await client.get_webhook_info()
        url = webhook_info.get('url')

        if not url or not url.startswith(settings.SERVER_URL):
            print('Webhook not set, setting one')
            await client.set_webhook(app.url_path_for('receive_update'))

    @app.on_event('startup')
    async def initialize_db():
        app.state.db_engine = create_db_engine(settings.db_uri)

    @app.on_event('shutdown')
    async def close_db():
        await app.state.db_engine.dispose()


def create_app():
    app = FastAPI()
    app.add_middleware(SessionMiddleware, secret_key=settings.SERVER_SECRET)
    app.include_router(bot_router, prefix='/bot')
    app.include_router(api_router, prefix='/api')

    setup_event_handlers(app)
    return app
