from sqlalchemy import select, desc, delete, literal
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas import TreatOut
from perekrestok.parser import PerekrestokParser, ProductData
from storage.models import (
    User,
    Shop,
    ShopLocation,
    Product,
    Price,
    Treat,
)


async def list_shops(session: AsyncSession):
    return (await session.scalars(select(Shop))).all()


async def get_shop_id(session: AsyncSession, url: str) -> Shop:
    query = (
        select(Shop.id)
        .where(literal(url).regexp_match(Shop.url_rule))
    )
    return (await session.scalars(query)).first()


async def get_user_shop_location(session: AsyncSession, shop_id: str, user_id: id):
    key = f'shop_{shop_id}_location'
    subquery = (
        select(User.meta[key].label('location_id'))
        .filter_by(id=user_id)
    ).subquery()

    query = (
        select(ShopLocation)
        .where(ShopLocation.location_id == subquery.c.location_id)
    )
    return (await session.scalars(query)).first()


async def list_treats(session: AsyncSession, user_id: int):
    latest_price_subquery = (
        select(
            Price.price,
            Price.old_price,
            Price.product_id
        )
        .order_by(desc(Price.created_at))
        .limit(1)
    ).subquery('latest_price')

    treats_query = (
        select(
            Treat.id,
            Product.title,
            Product.available,
            latest_price_subquery.c.price,
            latest_price_subquery.c.old_price,
            Product.url,
            ShopLocation.shop_id
        )
        .select_from(Product)
        .join(ShopLocation)
        .join(Treat)
        .join(latest_price_subquery)
        .where(Treat.user_id == user_id)
    )
    return (await session.execute(treats_query)).mappings().all()


async def delete_treat_by_id(session: AsyncSession, treat_id: int):
    await session.execute(delete(Treat).filter_by(id=treat_id))
    await session.commit()


async def treat_exists_for_user(session: AsyncSession, url: str, user_id: int) -> bool:
    subquery = (
        select(Treat)
        .join(Product)
        .where(
            Product.url.ilike(url),
            Treat.user_id == user_id)
    ).exists()

    query = select(literal(True)).where(subquery)
    return bool((await session.execute(query)).first())


async def get_product(session: AsyncSession, url: str, shop_location: ShopLocation):
    query = select(Product).filter_by(url=url, shop_location=shop_location)
    return (await session.scalars(query)).first()


async def get_latest_price(session: AsyncSession, product_id: int, shop_location_id: int):
    query = (
        select(Price)
        .join(Product)
        .where(
            Price.product_id == product_id,
            Product.shop_location_id == shop_location_id,
        )
        .order_by(desc(Price.created_at))
        .limit(1)
    )
    return (await session.scalars(query)).first()


async def get_product_data(product_url: str, shop_location: ShopLocation) -> ProductData:
    parser = PerekrestokParser()
    product_data = await parser.fetch(product_url, shop_location.location_id)

    if not product_data:
        raise RuntimeError(
            f'Could not fetch product data for {product_url=} using parser {parser.__class__.__name__}.'
        )
    return product_data


async def create_product(session: AsyncSession, product_url, shop_location: ShopLocation) -> tuple[Product, Price]:
    product_data = await get_product_data(product_url, shop_location)
    product = Product(
        title=product_data.title,
        available=product_data.available,
        url=product_url,
        shop_location=shop_location,
        meta=product_data.metadata
    )
    price = Price(
        price=product_data.price,
        old_price=product_data.old_price,
    )
    product.prices.append(price)
    session.add(product)
    await session.flush()

    return product, price


async def create_treat(session: AsyncSession, treat_url: str, user_id: int) -> TreatOut | None:
    if await treat_exists_for_user(session, treat_url, user_id):
        return

    shop_id = await get_shop_id(session, treat_url)

    if not shop_id:
        return

    shop_location = await get_user_shop_location(session, shop_id, user_id)
    product = await get_product(session, treat_url, shop_location)

    if not product:
        product, price = await create_product(session, treat_url, shop_location)
    else:
        price = await get_latest_price(session, product.id, shop_location.id)

    treat = Treat(user_id=user_id, product_id=product.id)
    session.add(treat)
    await session.commit()

    treat_out = TreatOut(
        id=treat.id,
        title=product.title,
        available=product.available,
        url=treat_url,
        price=price.price,
        old_price=price.old_price,
        shop_id=shop_id,
    )
    return treat_out
