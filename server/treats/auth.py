import time

from jwt import PyJWKClient, decode
from pydantic import BaseModel, Field
from auth0.v3.asyncify import asyncify
from auth0.v3.management import Users
from auth0.v3.authentication import GetToken

from config import settings

jwks_client = PyJWKClient(settings.auth0_jwks_url, lifespan=600)
Users = asyncify(Users)
GetToken = asyncify(GetToken)
get_token = GetToken(settings.AUTH0_DOMAIN)


class UserAccessToken(BaseModel):
    sub: str


class ManagementToken(BaseModel):
    access_token: str
    expires_in: int
    timestamp: int = Field(default_factory=time.monotonic)

    @property
    def is_expired(self):
        return time.monotonic() > self.timestamp + self.expires_in


class UserMetadata(BaseModel):
    language: str


class User(BaseModel):
    id: str = Field(alias='user_id')
    email: str = Field()
    metadata: UserMetadata = Field(alias='user_metadata', default_factory=dict)


def verify_token(token: str) -> UserAccessToken:
    signing_key = jwks_client.get_signing_key_from_jwt(token)
    data = decode(token, signing_key.key, algorithms=["RS256"], audience=settings.AUTH0_AUDIENCE)
    return UserAccessToken(**data)


def get_management_token():
    cached_token: ManagementToken | None = None

    async def fetch() -> ManagementToken:
        nonlocal cached_token

        if not cached_token or cached_token.is_expired:
            token = await get_token.client_credentials_async(
                settings.AUTH0_ID,
                settings.AUTH0_SECRET,
                settings.auth0_api_url
            )
            cached_token = ManagementToken(**token)
        return cached_token
    return fetch


get_management_token = get_management_token()


async def fetch_user(user_id: str) -> User:
    mgmt_token = await get_management_token()
    users = Users(settings.AUTH0_DOMAIN, mgmt_token.access_token)
    user = await users.get_async(user_id)
    return User(**user)
