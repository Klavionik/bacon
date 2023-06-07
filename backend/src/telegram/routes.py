from fastapi import APIRouter, Depends

from auth.manager import UserManager, get_user_manager
from auth.schemas import UserMeta, UserUpdate
from telegram.client import TelegramClient
from telegram.deps import decode_deep_link_token, get_telegram_client, make_deep_link
from telegram.permissions import check_allowed_users_dep
from telegram.schemas import DeepLink, InitData, Update

router = APIRouter()


@router.post("/update")
async def receive_update(
    update: Update,
    client: TelegramClient = Depends(get_telegram_client),
    user_manager: UserManager = Depends(get_user_manager),
):
    if update.is_deep_link:
        user_data = decode_deep_link_token(update.deep_link_token)
        user_id = int(user_data.split(":")[1])
        user = await user_manager.get(user_id)
        user_update = UserUpdate(
            meta=UserMeta(
                telegram_id=update.message.chat.id,
                telegram_notifications=True,
            )
        )
        await user_manager.update(user_update, user)
        msg = "Вы успешно подписались на уведомления."
        await client.send_message(update.message.chat.id, msg)
        return 200

    msg = "Привет! Чтобы использовать этого бота, нажми кнопку Меню внизу слева."
    await client.send_message(update.message.chat.id, msg)
    return 200


@router.post("/start", dependencies=[check_allowed_users_dep])
async def start(init_data: InitData):
    init_user = init_data.user
    ...
    return init_user


@router.get("/deep_link", response_model=DeepLink)
async def get_deep_link(deep_link: DeepLink = Depends(make_deep_link)):
    return deep_link
