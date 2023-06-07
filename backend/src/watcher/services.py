from sqlalchemy import Boolean, bindparam, select, update
from sqlalchemy.dialects.postgresql.json import JSONB
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import functions

from storage.models import Price, Product, ShopLocation, User, UserProduct

from .schemas import ProductInDB


async def get_products(session: AsyncSession, shop_id: int) -> list[ProductInDB]:
    latest_prices_cte = (
        select(
            Price.product_id,
            functions.max(Price.created_at).label("latest_date"),
        ).group_by(Price.product_id)
    ).cte()

    products_query = (
        select(
            Product.id,
            Product.title,
            Product.url,
            Product.available,
            Price.price,
            Price.old_price,
            ShopLocation.external_id,
        )
        .select_from(Product)
        .join(latest_prices_cte)
        .join(
            Price,
            (latest_prices_cte.c.latest_date == Price.created_at)
            & (Price.product_id == Product.id),
        )
        .join(ShopLocation)
        .where(ShopLocation.shop_id == shop_id)
    )
    result = await session.execute(products_query)
    return [ProductInDB(**data) for data in result.mappings()]


async def update_product_availability(session: AsyncSession, products: list[dict]):
    query = (
        update(Product)
        .where(Product.id == bindparam("p_id"))
        .values(available=bindparam("available"))
    )

    await session.execute(query, products)


async def get_users_to_notify(session: AsyncSession, product_id: int):
    tid = User.meta["telegram_id"].label("tid")
    notifications_enabled = (
        User.meta["telegram_notifications"].label("notifications_enabled").cast(JSONB).cast(Boolean)
    )
    query = (
        select(tid)
        .join(UserProduct, UserProduct.user_id == User.id)
        .where(UserProduct.product_id == product_id, notifications_enabled.is_(True))
    )
    return (await session.scalars(query)).all()
