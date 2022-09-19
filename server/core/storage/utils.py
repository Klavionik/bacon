from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine


def create_engine(db_uri: str, *, echo: bool = False) -> AsyncEngine:
    return create_async_engine(db_uri, echo=echo)
