from abc import ABC, abstractmethod
from typing import Iterable

from .models import ProductData


class BaseScraper(ABC):
    @abstractmethod
    def fetch(self, url: str, store_id: str) -> ProductData:
        pass

    @abstractmethod
    def fetch_all(self, urls: list[str], store_id: int) -> Iterable[ProductData]:
        pass
