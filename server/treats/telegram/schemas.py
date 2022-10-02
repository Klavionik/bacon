from pydantic import BaseModel, root_validator

from config import settings
from telegram.validation import validate_init_data


class Update(BaseModel):
    class Message(BaseModel):
        class Chat(BaseModel):
            id: int
        chat: Chat

    message: Message


class InitData(BaseModel):
    class User(BaseModel):
        id: int
        username: str
        language_code: str

    query_id: str
    user: User
    auth_date: str
    hash: str

    @root_validator(pre=True)
    def validate_integrity(cls, values):
        if not validate_init_data(values, settings.BOT_TOKEN):
            raise ValueError('Integrity check failed.')
        return values


class Token(BaseModel):
    token: str
