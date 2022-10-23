from fastapi import Request, Depends
from fastapi.security import OAuth2
from storage import create_db_session
from auth import verify_token, fetch_user, User, UserAccessToken


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


oauth2_scheme = Depends(OAuth2())


@Depends
def get_token(auth_header: str = oauth2_scheme) -> UserAccessToken:
    _, token = auth_header.split()
    return verify_token(token)


@Depends
async def get_user(token: UserAccessToken = get_token) -> User:
    user = await fetch_user(token.sub)
    return user
