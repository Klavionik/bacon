import base64
import hashlib
import hmac
from dataclasses import dataclass
from functools import cache
from urllib.parse import urljoin

import dacite
import httpx
from constance import config
from django.conf import settings
from django.urls import reverse
from loguru import logger

USER_HEADER = "dXNlcjo"


@dataclass
class Chat:
    id: int


@dataclass
class Message:
    text: str
    chat: Chat


@dataclass
class Update:
    message: Message

    @property
    def is_deep_link(self) -> bool:
        if self.message.text.startswith("/start"):
            entities = self.message.text.split()
            return len(entities) == 2 and entities[1].startswith(USER_HEADER)

    @property
    def deep_link_token(self) -> str | None:
        if not self.is_deep_link:
            return

        _, deep_link = self.message.text.split()
        return deep_link

    @classmethod
    def from_json(cls, payload: dict):
        return dacite.from_dict(data_class=cls, data=payload)


class Client:
    def __init__(self, base_url: str, token: str, server_url: str, server_secret: str):
        self.api_url = base_url.rstrip("/") + token
        self.server_url = server_url
        self.server_secret = server_secret

    def get_webhook_info(self) -> dict:
        return self.request("GET", "getWebhookInfo")

    def set_webhook(self, webhook_route: str) -> dict:
        data = {"url": urljoin(self.server_url, webhook_route), "secret_token": self.server_secret}
        return self.request("POST", "setWebhook", data)

    def send_message(self, chat_id: int, text: str, *, html: bool = False) -> dict:
        data = {"chat_id": chat_id, "text": text}

        if html:
            data.update(parse_mode="HTML")
        return self.request("POST", "sendMessage", data)

    def request(self, method: str, url: str, data: dict = None):
        with httpx.Client(base_url=self.api_url) as client:
            response = client.request(method, url, data=data)

        data = response.json()
        data_is_ok = data.get("ok")

        if not data_is_ok:
            raise RuntimeError(f"Request to {response.request.url} returned an error: {data}")
        return data.get("result")


@cache
def get_client() -> Client:
    return Client(
        base_url=config.TELEGRAM_API_URL,
        token=config.TELEGRAM_TOKEN,
        server_url=settings.SERVER_URL,
        server_secret=settings.SECRET_KEY,
    )


def initialize_webhook(client: Client):
    webhook_info = client.get_webhook_info()
    url = webhook_info.get("url")
    logger.info(f"Current webhook {url=}")

    if not url or not url.startswith(settings.SERVER_URL):
        cb_url = reverse("telegram_update", kwargs=dict(version="v1"))
        logger.info(f"Webhook not set, set this one: {cb_url}")
        client.set_webhook(cb_url)


def encode_deep_link_payload(payload: str) -> str:
    encoded = base64.urlsafe_b64encode(payload.encode()).decode()
    return encoded


def sign_deep_link_payload(payload: str) -> str:
    hasher = hashlib.blake2b(key=settings.SECRET_KEY.encode(), digest_size=16)
    hasher.update(payload.encode())
    signature = hasher.hexdigest()
    return signature


def verify_deep_link_token(token: str) -> bool:
    payload, signature = token.split("-")
    good_signature = sign_deep_link_payload(payload)
    return hmac.compare_digest(signature, good_signature)


def make_deep_link_token(payload: str) -> str:
    payload = encode_deep_link_payload(payload)
    signature = sign_deep_link_payload(payload)
    return f"{payload}-{signature}"


def make_deep_link(user) -> str:
    payload = f"user:{user.id}"
    token = make_deep_link_token(payload)
    link = f"https://t.me/GetBaconBot?start={token}"
    return link


def decode_deep_link_token(token: str) -> str:
    verified = verify_deep_link_token(token)

    if not verified:
        raise ValueError("Deep link signature mismatch.")

    payload, signature = token.split("-")
    return base64.urlsafe_b64decode(payload).decode()
