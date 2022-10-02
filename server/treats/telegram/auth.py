import jwt

from config import settings


def create_token(user_id: int) -> str:
    return jwt.encode(dict(sub=user_id), settings.SERVER_SECRET, algorithm='HS256')
