from sqlalchemy import select, desc, delete, literal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import functions

from api import schemas
from perekrestok.parser import PerekrestokParser, ProductData
from storage.models import (
    Shop,
    ShopLocation,
    Product,
    Price,
    Treat,
    UserShopLocation,
)


async def list_shops(session: AsyncSession):
    return (await session.scalars(select(Shop))).all()


async def get_shop(session: AsyncSession, url: str) -> Shop:
    query = (
        select(Shop)
        .where(literal(url).regexp_match(Shop.url_rule))
    )
    return (await session.scalars(query)).first()


async def list_treats(session: AsyncSession, user_id: int):
    latest_prices_subquery = (
        select(
            Price.price,
            Price.old_price,
            Price.product_id,
            functions.max(Price.created_at),
        )
        .group_by(Price.product_id)
    ).subquery('latest_price')

    treats_query = (
        select(
            Treat.id,
            Product.title,
            Product.available,
            latest_prices_subquery.c.price,
            latest_prices_subquery.c.old_price,
            Product.url,
            ShopLocation.shop_id,
            Shop.display_title,
        )
        .select_from(Product)
        .join(ShopLocation)
        .join(Shop)
        .join(Treat)
        .join(latest_prices_subquery)
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
    product_data = await parser.fetch(product_url, shop_location.external_id)

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


async def create_treat(session: AsyncSession, treat_url: str, user_id: int) -> schemas.TreatOut | None:
    if await treat_exists_for_user(session, treat_url, user_id):
        return

    shop = await get_shop(session, treat_url)

    if not shop:
        return

    user_shop_location = await get_user_shop_location_for_shop(session, user_id, shop.id)

    if not user_shop_location:
        return

    product = await get_product(session, treat_url, user_shop_location)

    if not product:
        product, price = await create_product(session, treat_url, user_shop_location)
    else:
        price = await get_latest_price(session, product.id, user_shop_location.id)

    treat = Treat(user_id=user_id, product_id=product.id)
    session.add(treat)
    await session.commit()

    treat_out = schemas.TreatOut(
        id=treat.id,
        title=product.title,
        available=product.available,
        url=treat_url,
        price=price.price,
        old_price=price.old_price,
        shop_id=shop.id,
        display_title=shop.display_title,
    )
    return treat_out


async def get_user_shop_locations_by_user(session: AsyncSession, user_id: int) -> list[ShopLocation]:
    query = (
        select(ShopLocation)
        .join(UserShopLocation)
        .where(UserShopLocation.user_id == user_id)
    )

    return (await session.scalars(query)).all()


async def get_user_shop_location_for_shop(
    session: AsyncSession,
    user_id: int,
    shop_id: int
) -> ShopLocation | None:
    query = (
        select(ShopLocation)
        .join(UserShopLocation)
        .where(UserShopLocation.user_id == user_id, UserShopLocation.shop_id == shop_id)
    )

    return (await session.scalars(query)).first()


async def ensure_shop_location(session: AsyncSession, shop_location: schemas.ShopLocationSuggestion):
    select_query = select(ShopLocation.id).filter_by(
        external_id=shop_location.external_id,
        shop_id=shop_location.shop_id
    )

    result = (await session.scalars(select_query)).first()

    if result:
        return result

    shop_location = ShopLocation(**shop_location.dict())
    session.add(shop_location)
    await session.flush([shop_location])
    return shop_location.id


async def save_user_shop_locations(
    session: AsyncSession,
    user_id: int,
    locations: list[schemas.ShopLocationSuggestion]
):
    await drop_user_shop_locations(session, user_id)

    for location in locations:
        location_id = await ensure_shop_location(session, location)
        user_shop_location = UserShopLocation(
            user_id=user_id,
            shop_location_id=location_id,
            shop_id=location.shop_id
        )
        session.add(user_shop_location)

    await session.commit()
    return locations


async def drop_user_shop_locations(session: AsyncSession, user_id: int):
    query = delete(UserShopLocation).where(UserShopLocation.user_id == user_id)
    await session.execute(query)
