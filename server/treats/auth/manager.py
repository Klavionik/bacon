from fastapi import Depends
from fastapi_users import IntegerIDMixin, BaseUserManager, InvalidPasswordException
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from config import settings
from storage.models import User
from .db import get_user_db
from .schemas import UserCreate

MIN_PASSWORD_LENGTH = 8


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = settings.SERVER_SECRET
    verification_token_secret = settings.SERVER_SECRET

    async def validate_password(
        self,
        password: str,
        user: UserCreate | User,
    ):
        if len(password) < MIN_PASSWORD_LENGTH:
            raise InvalidPasswordException(f"The password should have at least {MIN_PASSWORD_LENGTH} characters.")

        if password != user.repeat_password:
            raise InvalidPasswordException("'password' field should match 'repeat_password' field.")


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)
