from typing import Generator

from sqlalchemy import select, bindparam, update
from sqlalchemy.sql import functions
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from storage.models import Product, Price, ShopLocation
from storage.utils import create_db_engine, create_db_session
from perekrestok.parser import PerekrestokParser
from .schemas import Product as ProductSchema
from .utils import price_changed

engine = create_db_engine(settings.db_uri)
Session = create_db_session(engine)


async def get_products(session: AsyncSession, shop_id: int) -> Generator[ProductSchema, None, None]:
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
    return (ProductSchema(**data) for data in result.mappings())


async def update_perekrestok_products():
    parser = PerekrestokParser()
    update_availability_query = (
        update(Product)
        .where(Product.id == bindparam('p_id'))
        .values(available=bindparam('available'))
    )
    to_update = []
    updated_prices = 0

    async with Session() as session:
        products = await get_products(session, shop_id=1)

        for product in products:
            new_product = await parser.fetch(product.url, product.shop_location_external_id)

            if price_changed(product, new_product):
                price = Price(
                    price=new_product.price,
                    old_price=new_product.old_price,
                    product_id=product.id
                )
                session.add(price)
                updated_prices += 1
            elif new_product.available != product.available:
                to_update.append({'p_id': product.id, 'available': new_product.available})

        if to_update:
            await session.execute(update_availability_query, to_update)

        await session.commit()

        print(f'Updated product price: {updated_prices}')
        print(f'Update availability: {len(to_update)}')

