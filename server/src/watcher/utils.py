import asyncio
from functools import wraps

from .schemas import ProductInDB
from perekrestok.parser import ProductData, PerekrestokParser


def is_price_changed(product: ProductInDB, new_product: ProductData) -> bool:
    return new_product.price != product.price or new_product.old_price != product.old_price


def is_availablity_changed(product: ProductInDB, new_product: ProductData) -> bool:
    return new_product.available != product.available


def get_parser(shop_id: int):
    # For now return only PerekrestokParser.
    return PerekrestokParser()


def async_task(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        loop.run_until_complete(func(*args, **kwargs))
    return wrapper
