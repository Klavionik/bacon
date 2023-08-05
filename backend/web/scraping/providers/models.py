from dataclasses import dataclass, field
from typing import Any


@dataclass
class ProductData:
    title: str
    available: bool
    price: float
    old_price: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Store:
    id: str | int
    title: str
    address: str
