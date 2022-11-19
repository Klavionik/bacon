from datetime import datetime

from loguru import logger
from mako.template import Template
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from telegram.deps import get_telegram_client
from watcher import products_update
from watcher.schemas import ProductUpdate
from watcher.services import get_users_to_notify

product_update_template_path = settings.ROOT_DIR / 'watcher' / 'product_update.mako'
product_update_template = Template(filename=str(product_update_template_path))


def create_product_update_notification(shop: str, product_after: ProductUpdate, timestamp: datetime) -> str:
    context = dict(
        **product_after.dict(),
        shop=shop,
        timestamp=timestamp.strftime('%x %X'),
        discount=product_after.discount,
        had_discount=product_after.had_discount,
    )
    return product_update_template.render(**context)


async def send_product_update_notification(
    chat_id: int,
    shop: str,
    product_after: ProductUpdate,
    timestamp: datetime,
):
    telegram = get_telegram_client()
    message = create_product_update_notification(shop, product_after, timestamp)
    await telegram.send_message(chat_id, message, markdown=True)


@products_update.connect
async def notify_on_product_update(
    session: AsyncSession,
    op_id: str,
    shop: str,
    products: list[ProductUpdate],
    timestamp: datetime
):
    if not len(products):
        return

    logger.info(f"Notify on product update. Update OpID was {op_id}.")

    for product in products:
        users = await get_users_to_notify(session, product.id)
        logger.debug(f"Notify {len(users)} users, {product.id=}.")

        for telegram_id in users:
            await send_product_update_notification(telegram_id, shop, product, timestamp)
