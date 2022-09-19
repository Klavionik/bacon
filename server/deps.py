import fastapi
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncConnection
from core.repositories import TreatRepository, ShopRepository, UserRepository, ProductRepository, PriceRepository


async def get_db_connection(request: fastapi.Request):
    engine: AsyncEngine = request.app.state.db_engine
    connection = await engine.connect()

    try:
        yield connection
    finally:
        await connection.close()


async def get_treat_repo(connection: AsyncConnection = fastapi.Depends(get_db_connection)) -> TreatRepository:
    return TreatRepository(connection)


async def get_shop_repo(connection: AsyncConnection = fastapi.Depends(get_db_connection)) -> ShopRepository:
    return ShopRepository(connection)


async def get_user_repo(connection: AsyncConnection = fastapi.Depends(get_db_connection)) -> UserRepository:
    return UserRepository(connection)


async def get_product_repo(connection: AsyncConnection = fastapi.Depends(get_db_connection)) -> ProductRepository:
    return ProductRepository(connection)


async def get_price_repo(connection: AsyncConnection = fastapi.Depends(get_db_connection)) -> PriceRepository:
    return PriceRepository(connection)
