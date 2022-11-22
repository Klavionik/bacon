from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from auth.routes import router as auth_router
from api.routes import router as api_router
from storage import create_db_engine
from perekrestok.client import PerekrestokClient
from telegram.deps import get_telegram_client
from telegram.routes import router as bot_router
from config import settings
from telemetry import configure_sentry, configure_logger


async def healthcheck():
    return Response(status_code=200, content="OK")


def setup_event_handlers(app):
    @app.on_event('startup')
    async def on_startup():
        client = get_telegram_client()
        webhook_info = await client.get_webhook_info()
        url = webhook_info.get('url')

        if not url or not url.startswith(settings.server_url):
            print('Webhook not set, setting one')
            await client.set_webhook(app.url_path_for('receive_update'))

    @app.on_event('startup')
    async def initialize_db():
        app.state.db_engine = create_db_engine(settings.db_uri)

    @app.on_event('shutdown')
    async def close_db():
        await app.state.db_engine.dispose()

    @app.on_event('startup')
    async def initialize_shops():
        perekrestok = PerekrestokClient(settings.PEREKRESTOK_API_URL)
        app.state.shop_clients = {1: perekrestok}


def create_app():
    app = FastAPI()
    app.add_middleware(SessionMiddleware, secret_key=settings.SERVER_SECRET)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ALLOWED_ORIGIN,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(bot_router, prefix='/bot')
    app.include_router(api_router, prefix='/api')
    app.include_router(auth_router, prefix='/auth')
    app.router.get('/health')(healthcheck)

    setup_event_handlers(app)
    configure_sentry()
    configure_logger()
    return app