import asyncio

from watcher.tasks import update_perekrestok_products

if __name__ == '__main__':
    asyncio.run(update_perekrestok_products())
