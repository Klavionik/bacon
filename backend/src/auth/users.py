from fastapi_users import FastAPIUsers

from auth.backend import auth_backend
from auth.manager import get_user_manager
from storage.models import User

users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


get_user = users.current_user(active=True)
