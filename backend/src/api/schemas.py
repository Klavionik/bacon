from pydantic import BaseModel, HttpUrl, Field


class UserProductInput(BaseModel):
    url: HttpUrl


class Shop(BaseModel):
    id: int
    title: str
    display_title: str
    url_rule: str

    class Config:
        orm_mode = True


class ShopLocation(BaseModel):
    id: int
    title: str
    address: str
    external_id: int
    shop_id: int

    class Config:
        orm_mode = True


class ShopLocationSuggestion(BaseModel):
    title: str
    address: str
    external_id: int
    shop_id: int


class UserProductOutput(BaseModel):
    id: int
    title: str
    available: bool
    url: str
    price: float
    old_price: float | None
    shop_id: int
    shop_display_title: str = Field(alias='display_title')

    class Config:
        orm_mode = True
