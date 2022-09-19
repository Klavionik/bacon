from .repositories import (
    ShopRepository,
    ProductRepository,
    PriceRepository,
    TreatRepository,
    RecordNotFound
)
from .schemas import TreatOut
from .scraper import scraper


class TreatAlreadyExists(Exception):
    pass


async def add_treat(
        user_id: int,
        url: str,
        shop_repo: ShopRepository,
        product_repo: ProductRepository,
        price_repo: PriceRepository,
        treat_repo: TreatRepository,
) -> TreatOut:
    if await treat_repo.exists_by_url_and_user(url, user_id):
        raise TreatAlreadyExists

    shop = await shop_repo.get_by_url(url)

    try:
        product = await product_repo.get_by_url(url)
        price = await price_repo.get_latest_by_product_id(product.id)
    except RecordNotFound:
        with scraper:
            product_data = scraper.fetch(url)

        product = await product_repo.create(product_data.title, url, shop.id)
        price = await price_repo.create(product_data.price, product_data.last_price, product.id)

    treat = await treat_repo.create(user_id, product.id)
    await product_repo.commit()
    await price_repo.commit()
    await treat_repo.commit()
    return TreatOut(
        id=treat.id,
        title=product.title,
        url=product.url,
        price=price.price,
        last_price=price.last_price,
        shop_id=shop.id,
    )
