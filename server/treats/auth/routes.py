from auth.users import users
from auth.schemas import UserCreate, UserRead, UserUpdate
from auth.backend import auth_backend
from fastapi.routing import APIRouter

register_router = users.get_register_router(UserRead, UserCreate)
auth_router = users.get_auth_router(auth_backend)
reset_password_router = users.get_reset_password_router()
users_router = users.get_users_router(UserRead, UserUpdate)


router = APIRouter()
router.include_router(register_router)
router.include_router(auth_router)
router.include_router(reset_password_router)
router.include_router(users_router)
