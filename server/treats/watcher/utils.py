from .schemas import Product
from perekrestok.parser import ProductData


def price_changed(product: Product, new_product: ProductData):
    return new_product.price != product.price or new_product.old_price != product.old_price
