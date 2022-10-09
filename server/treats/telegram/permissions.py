from fastapi import Header, HTTPException, Depends

from config import settings
from telegram.schemas import InitData

TOKEN_HEADER = 'X-Telegram-Bot-Api-Secret-Token'


def verify_token(token: str = Header(alias=TOKEN_HEADER)):
    if token != settings.SERVER_SECRET:
        detail = f'{TOKEN_HEADER} header doesn\'t match.'
        raise HTTPException(status_code=403, detail=detail)


def check_allowed_users(init_data: InitData):
    allowed_users = settings.ALLOWED_USERS
    username = init_data.user.username

    if len(allowed_users) and username not in allowed_users:
        detail = f'{username} is not allowed to use this app.'
        raise HTTPException(status_code=403, detail=detail)


verify_token_dep = Depends(verify_token)
check_allowed_users_dep = Depends(check_allowed_users)
