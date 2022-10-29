from pydantic import BaseModel, root_validator, Field

from config import settings
from telegram.validation import validate_init_data

USER_HEADER = 'dXNlcjo'


class Update(BaseModel):
    class Message(BaseModel):
        class Chat(BaseModel):
            id: int

        chat: Chat
        text: str

    message: Message

    @property
    def is_deep_link(self) -> bool:
        if self.message.text.startswith('/start'):
            entities = self.message.text.split()
            if len(entities) == 2 and entities[1].startswith(USER_HEADER):
                return True
        return False

    @property
    def deep_link_token(self) -> str | None:
        if not self.is_deep_link:
            return

        _, deep_link = self.message.text.split()
        return deep_link


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


class DeepLink(BaseModel):
    link: str
