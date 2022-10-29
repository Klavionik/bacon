from functools import lru_cache
import hashlib
import hmac
import base64
from fastapi import Depends

from auth import get_user
from config import settings
from storage.models import User
from telegram.client import TelegramClient
from telegram.schemas import DeepLink


@lru_cache
def get_telegram_client():
    return TelegramClient(
        base_url=settings.TELEGRAM_BASE_URL,
        token=settings.BOT_TOKEN,
        server_url=settings.SERVER_URL,
        server_secret=settings.SERVER_SECRET,
    )


def encode_deep_link_payload(payload: str) -> str:
    encoded = base64.urlsafe_b64encode(payload.encode()).decode()
    return encoded


def sign_deep_link_payload(payload: str) -> str:
    hasher = hashlib.blake2b(key=settings.SERVER_SECRET.encode(), digest_size=16)
    hasher.update(payload.encode())
    signature = hasher.hexdigest()
    return signature


def verify_deep_link_token(token: str) -> bool:
    payload, signature = token.split('-')
    good_signature = sign_deep_link_payload(payload)
    return hmac.compare_digest(signature, good_signature)


def make_deep_link_token(payload: str) -> str:
    payload = encode_deep_link_payload(payload)
    signature = sign_deep_link_payload(payload)
    return f'{payload}-{signature}'


def make_deep_link(user: User = Depends(get_user)) -> DeepLink:
    payload = f'user:{user.id}'
    token = make_deep_link_token(payload)
    link = f"https://t.me/MyTreatsBot?start={token}"
    return DeepLink(link=link)


def decode_deep_link_token(token: str) -> str:
    verified = verify_deep_link_token(token)

    if not verified:
        raise ValueError('Deep link signature mismatch.')

    payload, signature = token.split('-')
    return base64.urlsafe_b64decode(payload).decode()

