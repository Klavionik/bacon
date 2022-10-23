from fastapi import APIRouter

from telegram.auth import create_token
from telegram.deps import get_telegram_client
from telegram.permissions import verify_token_dep, check_allowed_users_dep
from telegram.schemas import Update, InitData, Token

router = APIRouter()


@router.post('/update', dependencies=[verify_token_dep])
async def receive_update(update: Update):
    client = get_telegram_client()
    msg = 'Привет! Чтобы использовать этого бота, нажми кнопку Меню внизу слева.'
    await client.send_message(update.message.chat.id, msg)
    return 200


@router.post('/start', dependencies=[check_allowed_users_dep])
async def start(init_data: InitData) -> Token:
    init_user = init_data.user
    ...
    return init_user
