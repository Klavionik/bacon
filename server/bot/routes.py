from fastapi import APIRouter, Depends

from core.repositories import UserRepository, RecordNotFound
from .auth import create_token
from .deps import get_telegram_client
from .permissions import verify_token_dep, check_whitelist_dep
from .schemas import Update, InitData, Token
from ..deps import get_user_repo

router = APIRouter()


@router.post('/update', dependencies=[verify_token_dep])
async def receive_update(update: Update):
    client = get_telegram_client()
    msg = 'Привет! Чтобы использовать этого бота, нажми кнопку Меню внизу слева.'
    await client.send_message(update.message.chat.id, msg)
    return 200


@router.post('/start', dependencies=[check_whitelist_dep])
async def start(init_data: InitData, user_service: UserRepository = Depends(get_user_repo)) -> Token:
    init_user = init_data.user

    try:
        user = await user_service.get(telegram_id=init_user.id)
        token = create_token(user.id)
        token = Token(token=token)
    except RecordNotFound:
        user_id = await user_service.create(init_user.username, init_user.id, init_user.language_code)
        await user_service.commit()
        token = create_token(user_id)
        token = Token(token=token)

    return token
