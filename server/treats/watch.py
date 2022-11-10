import asyncio

from huey import FileHuey, MemoryHuey, crontab
from loguru import logger
from sqlalchemy import select

from config import settings
from storage import create_db_engine, create_db_session
from storage.models import Shop
from watcher.api import update_products

engine = create_db_engine(settings.db_uri)
Session = create_db_session(engine)


if settings.DEBUG:
    huey = MemoryHuey()
    schedule = crontab()
else:
    huey = FileHuey('/var/lib/huey/data')
    schedule = crontab(minute='0', hour='*/1')


@huey.periodic_task(schedule)
def run_update_products():
    async def _run():
        async with Session() as session:
            shops = await session.scalars(select(Shop.id))

            for shop_id in shops:
                await update_products(session, shop_id)

    asyncio.run(_run())
