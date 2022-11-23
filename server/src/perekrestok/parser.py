import logging
import re
from typing import Any, AsyncGenerator

from perekrestok.client import PerekrestokClient
from pydantic import BaseModel, PositiveFloat

log = logging.getLogger(__name__)

parsers = []

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'


class ProductData(BaseModel):
    title: str
    available: bool
    price: PositiveFloat
    old_price: PositiveFloat | None = None
    metadata: dict[str, Any] = {}


class PerekrestokParser:
    name = 'Перекресток'
    url_rule = re.compile(r'^https://(w{3}\.)?perekrestok\.ru/cat/.+$')

    async def fetch_all(self, urls: list[str], shop_location_external_id: int) -> AsyncGenerator[ProductData, None]:
        client = PerekrestokClient('https://www.perekrestok.ru/api/customer/1.4.1.0')

        async with client:
            await client.set_shop(shop_location_external_id)

            for url in urls:
                plu = self._extract_plu_from_url(url)
                data = await client.fetch_product_data(plu)

                if not data:
                    continue

                try:
                    product = self._parse_product_data(data)
                except Exception as exc:
                    log.warning(f'Cannot parse {url=} with following exception: %s.', exc)
                    continue

                yield product

    async def fetch(self, url: str, shop_location_external_id: int) -> ProductData:
        client = PerekrestokClient('https://www.perekrestok.ru/api/customer/1.4.1.0')

        async with client:
            await client.set_shop(shop_location_external_id)
            plu = self._extract_plu_from_url(url)
            data = await client.fetch_product_data(plu)

            try:
                product = self._parse_product_data(data)
                return product
            except Exception as exc:
                log.warning(f'Cannot parse {url=} with following exception: %s.', exc)

    @staticmethod
    def _parse_product_data(data: dict[str, Any]) -> ProductData:
        content = data.get('content')
        price_tag = content.get('priceTag')
        plu = content.get('plu')

        title = content.get('title')
        available = not content.get('balanceState') == 'sold-out'

        if price_tag is not None:
            price = price_tag.get('price')
            old_price = price_tag.get('grossPrice')
        else:
            price = content.get('medianPrice')
            old_price = None

        product = ProductData(
            title=title,
            available=available,
            price=price / 100,
            old_price=old_price / 100 if old_price else old_price,
            metadata=dict(plu=plu)
        )

        return product

    @staticmethod
    def _extract_plu_from_url(url: str) -> int:
        return int(url.rsplit('-', maxsplit=1)[-1])
