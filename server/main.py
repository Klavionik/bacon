from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from core.storage import create_engine
from .api.routes import router as api_router
from .bot.client import get_client
from .bot.routes import router as bot_router
from .settings import settings

engine = create_engine(settings.DB_URI, echo=True)


def setup_event_handlers(app):
    @app.on_event('startup')
    async def on_startup():
        client = get_client()
        webhook_info = await client.get_webhook_info()
        url = webhook_info.get('url')

        if not url or not url.startswith(settings.SERVER_URL):
            print('Webhook not set, setting one')
            await client.set_webhook(app.url_path_for('receive_update'))


def create_app():
    app = FastAPI()
    app.add_middleware(SessionMiddleware, secret_key=settings.SERVER_SECRET)
    app.include_router(bot_router, prefix='/bot')
    app.include_router(api_router, prefix='/api')

    setup_event_handlers(app)

    app.state.db_engine = engine
    return app
