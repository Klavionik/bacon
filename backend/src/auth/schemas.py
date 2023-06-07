from fastapi_users.schemas import BaseUser, BaseUserCreate, BaseUserUpdate
from pydantic import BaseModel


def to_lower_camel(string: str) -> str:
    camelised = []

    for i, word in enumerate(string.split("_")):
        if i == 0:
            camelised.append(word)
        else:
            camelised.append(word.capitalize())
    return "".join(camelised)


class UserMeta(BaseModel):
    telegram_id: int | None = None
    telegram_notifications: bool = False

    class Config:
        alias_generator = to_lower_camel
        allow_population_by_field_name = True


class UserCreate(BaseUserCreate):
    repeat_password: str
    meta: UserMeta = UserMeta()

    class Config:
        alias_generator = to_lower_camel
        allow_population_by_field_name = True


class UserRead(BaseUser[int]):
    meta: UserMeta

    class Config:
        alias_generator = to_lower_camel
        allow_population_by_field_name = True


class UserUpdate(BaseUserUpdate):
    meta: UserMeta

    class Config:
        alias_generator = to_lower_camel
        allow_population_by_field_name = True
