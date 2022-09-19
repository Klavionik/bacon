from pydantic import BaseModel, HttpUrl


class TokenData(BaseModel):
    sub: int


class TreatInput(BaseModel):
    url: HttpUrl
