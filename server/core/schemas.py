from typing import Any

from pydantic import BaseModel, HttpUrl, PositiveFloat
from datetime import date


class ParsedProduct(BaseModel):
    title: str
    available: bool
    price: PositiveFloat
    old_price: PositiveFloat | None = None
    metadata: dict[str, Any]


class Treat(BaseModel):
    id: int
    created_at: date
    user_id: int
    product_id: int


class Product(BaseModel):
    id: int
    title: str
    url: HttpUrl
    shop_id: int


class Price(BaseModel):
    id: int
    created_at: date
    price: PositiveFloat
    last_price: PositiveFloat | None = None


class User(BaseModel):
    id: int
    username: str
    telegram_id: int
    language_code: str


class Shop(BaseModel):
    id: int
    name: str
    link_pattern: str


class TreatOut(BaseModel):
    id: int
    title: str
    url: str
    price: float
    last_price: float | None
    shop_id: int
