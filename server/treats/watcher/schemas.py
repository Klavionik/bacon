from pydantic import BaseModel, Field


class ProductInDB(BaseModel):
    id: int
    title: str
    available: bool
    price: float
    old_price: float | None
    url: str
    shop_location_external_id: int = Field(alias='external_id')


class ProductUpdate(BaseModel):
    id: int
    title: str
    available: bool
    price_before: float
    price_old_before: float | None
    price_after: float
    price_old_after: float | None

    @property
    def discount(self) -> bool:
        return self.price_old_after is not None and self.price_after < self.price_old_after

    @property
    def had_discount(self) -> bool:
        return self.price_old_before is not None and self.price_before < self.price_old_before
