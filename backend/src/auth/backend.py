from fastapi_users.authentication import JWTStrategy, AuthenticationBackend, BearerTransport

from config import settings


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.SERVER_SECRET, lifetime_seconds=604800)  # A week.


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=BearerTransport(tokenUrl="auth/jwt/login"),
    get_strategy=get_jwt_strategy,
)
