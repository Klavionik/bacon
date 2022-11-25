from huey import RedisHuey, crontab
from sqlalchemy import select

from config import settings
from telemetry import configure_sentry, configure_logger
from storage import create_db_engine, create_db_session
from storage.models import Shop
from watcher.api import update_products
from watcher.utils import async_task

engine = create_db_engine(settings.db_uri)
Session = create_db_session(engine)

if settings.DEBUG:
    schedule = crontab()
else:
    schedule = crontab(minute='0', hour='*/1')

huey = RedisHuey(url=settings.queue_uri)

configure_logger()
configure_sentry()


@async_task
async def _run_update_products():
    async with Session() as session:
        shops = await session.scalars(select(Shop.id))

        for shop_id in shops:
            await update_products(session, shop_id)


@huey.periodic_task(schedule)
def run_update_products():
    _run_update_products()
