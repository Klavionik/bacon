from fastapi_users.schemas import BaseUserCreate, BaseUser, BaseUserUpdate


def to_lower_camel(string: str) -> str:
    camelised = []

    for i, word in enumerate(string.split('_')):
        if i == 0:
            camelised.append(word)
        else:
            camelised.append(word.capitalize())
    return ''.join(camelised)


class UserCreate(BaseUserCreate):
    repeat_password: str

    class Config:
        alias_generator = to_lower_camel


class UserRead(BaseUser[int]):
    pass


class UserUpdate(BaseUserUpdate):
    pass
