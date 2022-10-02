from fastapi import Request, Depends
from storage import create_db_session


@Depends
async def db_session(request: Request):
    engine = request.app.state.db_engine
    session = create_db_session(engine)()

    try:
        yield session
    finally:
        await session.close()
