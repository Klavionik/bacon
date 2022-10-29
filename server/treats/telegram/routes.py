from fastapi import APIRouter

from config import settings
from telegram.deps import get_telegram_client
from telegram.permissions import check_allowed_users_dep
from telegram.schemas import InitData

router = APIRouter()


@router.post('/update')
async def receive_update():
    client = get_telegram_client()
    msg = f'Привет! Чтобы использовать этого бота, нажми кнопку Меню внизу слева.'
    await client.send_message(settings.BOT_CHAT_ID, msg)
    return 200


@router.post('/start', dependencies=[check_allowed_users_dep])
async def start(init_data: InitData):
    init_user = init_data.user
    ...
    return init_user
