from typing import Any, Iterable

from loguru import logger

from ..base import BaseScraper
from ..models import ProductData
from .client import PerekrestokClient

USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/104.0.0.0 Safari/537.36"
)


class PerekrestokScraper(BaseScraper):
    def __init__(self, api_base_url: str, proxy: str | None = None):
        self.api_base_url = api_base_url
        self.proxy = proxy
        self.client = PerekrestokClient(self.api_base_url, self.proxy)

    def fetch_all(self, urls: list[str], store_id: str) -> Iterable[ProductData]:
        with self.client:
            self.client.set_store(store_id)

            for url in urls:
                plu = self._extract_plu_from_url(url)
                data = self.client.fetch_product_data(plu)

                if not data:
                    continue

                try:
                    product = self._parse_product_data(data)
                except Exception as exc:
                    logger.warning(f"Cannot parse {url=} with following exception: %s.", exc)
                    continue

                yield product

    def fetch(self, url: str, store_id: str) -> ProductData:
        with self.client:
            self.client.set_store(store_id)
            plu = self._extract_plu_from_url(url)
            data = self.client.fetch_product_data(plu)

            try:
                product = self._parse_product_data(data)
                return product
            except Exception as exc:
                logger.warning(f"Cannot parse {url=} with following exception: %s.", exc)

    @staticmethod
    def _parse_product_data(data: dict[str, Any]) -> ProductData:
        content = data.get("content")
        price_tag = content.get("priceTag")
        plu = content.get("plu")

        title = content.get("title")
        available = not content.get("balanceState") in ["sold-out", "no-stock"]

        if price_tag is not None:
            price = price_tag.get("price")
            old_price = price_tag.get("grossPrice")
        else:
            price = content.get("medianPrice")
            old_price = None

        product = ProductData(
            title=title,
            available=available,
            price=price / 100,
            old_price=old_price / 100 if old_price else old_price,
            metadata=dict(plu=plu),
        )

        return product

    @staticmethod
    def _extract_plu_from_url(url: str) -> int:
        return int(url.rsplit("-", maxsplit=1)[-1])
