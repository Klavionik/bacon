import jwt
from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader

from core.repositories import UserRepository, RecordNotFound
from core.schemas import User
from .schemas import TokenData
from ..settings import settings
from ..deps import get_user_repo

api_key = APIKeyHeader(name='Authorization')


async def get_current_user(
        token: str = Depends(api_key),
        user_repo: UserRepository = Depends(get_user_repo)
) -> User | None:
    scheme, token = token.split()

    try:
        payload = jwt.decode(token, settings.SERVER_SECRET, algorithms=['HS256'])
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=403, detail=f'Could not decode token: {str(e)}.')

    data = TokenData(**payload)

    try:
        user = await user_repo.get(user_id=data.sub)
    except RecordNotFound:
        raise HTTPException(status_code=403, detail='No such user found.')
    return user
