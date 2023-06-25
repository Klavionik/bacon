from abc import ABC, abstractmethod
from functools import singledispatchmethod
from typing import Iterable

from .models import ProductData


class BaseProvider(ABC):
    @singledispatchmethod
    @abstractmethod
    def fetch_product(self, urls: str, store_id: str) -> ProductData:
        pass

    @fetch_product.register
    @abstractmethod
    def _(self, urls: list, store_id: str) -> Iterable[ProductData]:
        pass

    @abstractmethod
    def fetch_stores(self, address: str):
        pass
