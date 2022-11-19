from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from deps import db_session
from storage.models import User


class UserDatabase(SQLAlchemyUserDatabase):
    async def create(self, create_dict):
        # Remove repeat_password after validation,
        # before saving the user to the database.
        create_dict.pop('repeat_password')
        return await super().create(create_dict)


async def get_user_db(session: AsyncSession = Depends(db_session)):
    yield UserDatabase(session, User)
