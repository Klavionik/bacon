from fastapi import Depends, Request

from storage import create_db_session


async def db_session(request: Request):
    engine = request.app.state.db_engine

    async with create_db_session(engine)() as session:
        yield session


@Depends
async def shop_client(request: Request, shop_id: int):
    """
    The only supported client for now is
    Perekrestok, so don't bother looking
    for the right one.
    """
    clients = request.app.state.shop_clients
    return clients[shop_id]
