from fastapi import Request, Depends
from storage import create_db_session
from perekrestok.client import PerekrestokClient
from config import settings


@Depends
async def db_session(request: Request):
    engine = request.app.state.db_engine
    session = create_db_session(engine)()

    try:
        yield session
    finally:
        await session.close()


@Depends
async def shop_client(request: Request, shop_id: int):
    """
    The only supported client for now is
    Perekrestok, so don't bother looking
    for the right one.
    """
    clients = request.app.state.shop_clients
    return clients[shop_id]
