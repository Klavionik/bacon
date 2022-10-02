from datetime import datetime

from pydantic import BaseModel, HttpUrl, PositiveFloat


class TokenData(BaseModel):
    sub: int


class TreatInput(BaseModel):
    url: HttpUrl


class Treat(BaseModel):
    id: int
    user_id: int
    product_id: int
    created_at: datetime


class Product(BaseModel):
    id: int
    title: str
    url: HttpUrl
    shop_location_id: int
    meta: dict


class Price(BaseModel):
    id: int
    price: PositiveFloat
    old_price: PositiveFloat | None = None
    created_at: datetime
    product_id: int


class User(BaseModel):
    id: int
    username: str
    language: str
    meta: dict

    class Config:
        orm_mode = True


class Shop(BaseModel):
    id: int
    name: str
    url_rule: str

    class Config:
        orm_mode = True


class ShopLocation(BaseModel):
    id: int
    address: str
    location_id: int
    shop_id: int


class TreatOut(BaseModel):
    id: int
    title: str
    available: bool
    url: str
    price: float
    old_price: float | None
    shop_id: int

    class Config:
        orm_mode = True
