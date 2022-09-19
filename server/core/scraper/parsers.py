import logging
import re
from typing import Any, AsyncGenerator, Type

from pydantic import BaseModel, PositiveFloat

from core.clients import PerekrestokClient

log = logging.getLogger(__name__)

parsers = []

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'


def register(cls):
    parsers.append(cls)
    return cls


class Product(BaseModel):
    title: str
    available: bool
    price: PositiveFloat
    old_price: PositiveFloat | None = None
    metadata: dict[str, Any] = {}


class ParserNotFound(Exception):
    pass


class BaseParser:
    name: str
    url_rule: re.Pattern

    def __init__(self, client: PerekrestokClient, context: dict[str, Any]):
        self.client = client
        self.context = context

    def fetch(self):
        raise NotImplementedError


@register
class PerekrestokParser(BaseParser):
    name = 'Перекресток'
    url_rule = re.compile(r'^https://(w{3}\.)?perekrestok\.ru/cat/.+$')

    async def fetch(self) -> AsyncGenerator[Product, None]:
        items: list[int] = self.context.get('items')
        shop_location_id: int = self.context.get('shop_location_id')

        async with self.client:
            await self.client.set_shop(shop_location_id)

            for item in items:
                data = await self.client.fetch_product_data(item)

                if not data:
                    continue

                try:
                    product = self._parse_product_data(data)
                except Exception as exc:
                    log.warning(f'Cannot parse {item=} with following exception: %s.', exc)
                    continue

                yield product

    @staticmethod
    def _parse_product_data(data: dict[str, Any]) -> Product:
        content = data.get('content')
        price_tag = content.get('priceTag')
        plu = content.get('plu')

        title = content.get('title')
        available = not content.get('balanceState') == 'sold-out'
        price = price_tag.get('price') / 100
        old_price = price_tag.get('grossPrice') / 100

        product = Product(
            title=title,
            available=available,
            price=price,
            old_price=old_price,
            metadata=dict(plu=plu)
        )

        return product


def get_parser_by_url(url: str) -> Type[BaseParser]:
    for parser in parsers:
        if parser.url_rule.match(url):
            return parser

        raise ParserNotFound
