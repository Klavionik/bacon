from sqlalchemy import select, delete, insert, desc, literal
from sqlalchemy.ext.asyncio import AsyncConnection

from core import schemas
from core.storage import users, shops, treats, products, prices


class RecordNotFound(Exception):
    pass


class BaseRepository:
    def __init__(self, connection: AsyncConnection):
        self.connection = connection

    async def commit(self):
        await self.connection.commit()

    async def rollback(self):
        await self.connection.rollback()


class ProductRepository(BaseRepository):
    async def create(self, title: str, url: str, shop_id: int) -> schemas.Product:
        query = insert(products)
        values = dict(title=title, url=url, shop_id=shop_id)
        result = await self.connection.execute(query, values)
        [pk] = result.inserted_primary_key
        values.update(id=pk)
        return schemas.Product(**values)

    async def get_by_url(self, url: str) -> schemas.Product:
        query = select(products).filter_by(url=url)
        result = (await self.connection.execute(query)).mappings().one_or_none()

        if not result:
            raise RecordNotFound(f'Product not found, {url=}.')

        return schemas.Product(**result)


class PriceRepository(BaseRepository):
    async def create(self, price: float, last_price: float | None, product_id: int) -> schemas.Price:
        query = insert(prices).returning(prices.c.created_at, prices.c.id)
        values = dict(price=price, last_price=last_price, product_id=product_id)
        result = await self.connection.execute(query, values)
        values.update(**result.mappings().one())
        return schemas.Price(**values)

    async def get_latest_by_product_id(self, product_id: int) -> schemas.Price:
        query = (
            select(prices)
            .filter_by(product_id=product_id)
            .order_by(desc(prices.c.created_at))
            .limit(1)
        )
        result = (await self.connection.execute(query)).mappings().one_or_none()

        if not result:
            raise RecordNotFound(f'Price not found, {product_id=}.')

        return schemas.Price(**result)


class TreatRepository(BaseRepository):
    async def list_by_user(self, user_id: int) -> list[schemas.TreatOut]:
        latest_price_subquery = (
            select(
                prices.c.price,
                prices.c.last_price
            )
            .order_by(desc(prices.c.created_at))
            .limit(1)
        ).subquery()

        query = (
            select(
                treats,
                products.c.title,
                latest_price_subquery.c.price,
                latest_price_subquery.c.last_price,
                products.c.url,
                shops.c.id.label('shop_id')
            )
            .select_from(treats)
            .join(products)
            .join(latest_price_subquery, treats.c.product_id == products.c.id)
            .join(shops)
            .where(treats.c.user_id == user_id)
        )

        result = await self.connection.execute(query)
        return [schemas.TreatOut(**treat) for treat in result.mappings()]

    async def delete(self, treat_id: int) -> None:
        query = delete(treats).filter_by(id=treat_id)
        await self.connection.execute(query)
        await self.connection.commit()

    async def create(self, user_id: int, product_id: int) -> schemas.Treat:
        query = insert(treats).returning(treats.c.id, treats.c.created_at)
        values = dict(user_id=user_id, product_id=product_id)
        result = await self.connection.execute(query, values)
        values.update(result.mappings().one())
        return schemas.Treat(**values)

    async def exists_by_url_and_user(self, url: str, user_id: int) -> bool:
        query = (
            select(
                literal(1).label('a')
            )
            .select_from(treats)
            .join(products)
            .filter(products.c.url.ilike(url), treats.c.user_id == user_id)
            .limit(1)
        )
        result = (await self.connection.execute(query))
        return bool(result.scalars().first())

    async def exists(self, treat_id: int, user_id: int) -> bool:
        query = (
            select(
                literal(1).label('a')
            )
            .select_from(treats)
            .filter_by(id=treat_id, user_id=user_id)
            .limit(1)
        )
        result = await self.connection.execute(query)
        return bool(result.scalars().first())


class UserRepository(BaseRepository):
    async def create(self, username: str, telegram_id: int, language_code: str) -> int:
        values = dict(username=username, telegram_id=telegram_id, language_code=language_code)
        result = await self.connection.execute(insert(users, values))
        return result.inserted_primary_key[0]

    async def get(self, *, user_id: int = None, telegram_id: int = None) -> schemas.User:
        no_id = not (user_id or telegram_id)
        both_ids = user_id and telegram_id

        if no_id or both_ids:
            raise ValueError('You must pass either a user_id or a telegram_id.')

        if user_id:
            query = select(users).filter_by(id=user_id)
        else:
            query = select(users).filter_by(telegram_id=telegram_id)

        result = (await self.connection.execute(query)).mappings().one_or_none()

        if result is None:
            params = query.compile().params
            raise RecordNotFound(f'User not found, filter: {params}.')

        return schemas.User(**result)


class ShopRepository(BaseRepository):
    async def list(self) -> list[schemas.Shop]:
        query = select(shops)
        result = await self.connection.execute(query)
        return [schemas.Shop(**shop) for shop in result.mappings()]

    async def get_by_url(self, url: str) -> schemas.Shop:
        query = select(shops).where(literal(url).regexp_match(shops.c.link_pattern))
        result = (await self.connection.execute(query)).mappings().one_or_none()

        if result is None:
            raise RecordNotFound(f'Shop not found, {url=}.')

        return schemas.Shop(**result)
