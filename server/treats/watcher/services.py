from typing import Generator

from sqlalchemy import select, update, bindparam, Boolean
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import functions

from storage.models import Product, Price, ShopLocation, User, Treat
from .schemas import ProductInDB


async def get_products(session: AsyncSession, shop_id: int) -> Generator[ProductInDB, None, None]:
    latest_prices_subquery = (
        select(
            Price.price,
            Price.old_price,
            Price.product_id,
            functions.max(Price.created_at),
        )
        .group_by(Price.product_id)
    ).subquery('latest_prices')

    products_query = (
        select(
            Product.id,
            Product.title,
            latest_prices_subquery.c.price,
            latest_prices_subquery.c.old_price,
            Product.url,
            Product.available,
            ShopLocation.external_id,
        )
        .select_from(Product)
        .join(latest_prices_subquery)
        .join(ShopLocation)
        .where(ShopLocation.shop_id == shop_id)
    )
    result = await session.execute(products_query)
    return (ProductInDB(**data) for data in result.mappings())


async def update_product_availability(session: AsyncSession, products: list[dict]):
    query = (
        update(Product)
        .where(Product.id == bindparam('p_id'))
        .values(available=bindparam('available'))
    )

    await session.execute(query, products)


async def get_users_to_notify(session: AsyncSession, product_id: int):
    tid = User.meta['telegram_id'].label('tid')
    notifications_enabled = User.meta['telegram_notifications'].label('notifications_enabled').cast(Boolean)
    query = (
        select(tid)
        .join(Treat, Treat.user_id == User.id)
        .where(Treat.product_id == product_id, notifications_enabled.is_(True))
    )
    return (await session.scalars(query)).all()
