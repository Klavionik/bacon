import asyncio
from huey import FileHuey, MemoryHuey, crontab
from watcher.tasks import update_perekrestok_products
from config import settings

if settings.DEBUG:
    huey = MemoryHuey()
    schedule = crontab()
else:
    huey = FileHuey('/var/lib/huey/data')
    schedule = crontab(minute='0', hour='*/1')


@huey.periodic_task(schedule)
def run_update_perekrestok_prices():
    asyncio.run(update_perekrestok_products())
