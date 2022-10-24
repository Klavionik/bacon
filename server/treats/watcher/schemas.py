from pydantic import BaseModel, Field


class Product(BaseModel):
    id: int
    available: bool
    price: float
    old_price: float | None
    url: str
    shop_location_external_id: int = Field(alias='external_id')
