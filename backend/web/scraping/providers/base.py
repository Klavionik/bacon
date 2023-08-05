from abc import ABC, abstractmethod
from functools import singledispatchmethod
from typing import Iterable

from .models import ProductData, Store


class BaseProvider(ABC):
    @singledispatchmethod
    @abstractmethod
    def fetch_products(self, urls: str, store_id: str) -> ProductData:
        pass

    @fetch_products.register
    @abstractmethod
    def _(self, urls: list, store_id: str) -> Iterable[ProductData]:
        pass

    @abstractmethod
    def fetch_stores(self, address: str) -> Iterable[Store]:
        pass
