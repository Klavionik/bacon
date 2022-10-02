from fastapi import Header, HTTPException, Depends

from config import settings
from telegram.schemas import InitData

TOKEN_HEADER = 'X-Telegram-Bot-Api-Secret-Token'


def verify_token(token: str = Header(alias=TOKEN_HEADER)):
    if token != settings.SERVER_SECRET:
        detail = f'{TOKEN_HEADER} header doesn\'t match.'
        raise HTTPException(status_code=403, detail=detail)


def check_whitelist(init_data: InitData):
    whitelist = settings.WHITELIST
    username = init_data.user.username

    if len(whitelist) and username not in whitelist:
        detail = f'{username} is not allowed to use this app.'
        raise HTTPException(status_code=403, detail=detail)


verify_token_dep = Depends(verify_token)
check_whitelist_dep = Depends(check_whitelist)
