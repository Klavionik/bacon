from datetime import datetime
from uuid import uuid4
from zoneinfo import ZoneInfo

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from storage.models import Price, Shop
from watcher.schemas import ProductUpdate
from watcher.services import get_products, update_product_availability
from watcher.signals import products_update
from watcher.utils import get_parser, is_availablity_changed, is_price_changed

UTC = ZoneInfo("UTC")


async def update_products(session: AsyncSession, shop_id: int):
    op_id = uuid4().hex
    logger.info(f"Update products. OpID {op_id}, shop ID {shop_id}.")

    shop = await session.get(Shop, shop_id)
    parser = get_parser(shop_id)

    availablity_updated = []
    updated = []

    products = await get_products(session, shop_id=shop_id)

    logger.info(f"Try to update {len(products)} products.")

    for product in products:
        new_product = await parser.fetch(product.url, product.shop_location_external_id)
        price_changed = is_price_changed(product, new_product)
        availablity_changed = is_availablity_changed(product, new_product)

        if price_changed or availablity_changed:
            updated.append(
                ProductUpdate(
                    id=product.id,
                    title=product.title,
                    price_before=product.price,
                    price_after=new_product.price,
                    price_old_before=product.old_price,
                    price_old_after=new_product.old_price,
                    available=new_product.available,
                )
            )

            if price_changed:
                price = Price(
                    price=new_product.price, old_price=new_product.old_price, product_id=product.id
                )
                session.add(price)
                logger.info(f"Price change: {product.id=}.")
            elif availablity_changed:
                logger.info(
                    f"Availablity change: from {product.available} to {new_product.available}."
                )
                availablity_updated.append({"p_id": product.id, "available": new_product.available})

    if len(availablity_updated):
        await update_product_availability(session, availablity_updated)

    await session.commit()

    logger.info(
        f"Finished updating products. "
        f"OpID {op_id}, shop ID {shop_id}. Updated {len(updated)} products."
    )

    timestamp = datetime.now(tz=UTC)
    await products_update.emit(
        session=session, op_id=op_id, shop=shop.display_title, products=updated, timestamp=timestamp
    )
