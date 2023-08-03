import argparse

from loguru import logger

from .provider import PerekrestokProvider

DEFAULT_API_BASE_URL = "https://www.perekrestok.ru/api/customer/1.4.1.0"


def main(url: str, store_id: str, api_base_url: str, proxy: str | None):
    provider = PerekrestokProvider(api_base_url, proxy)
    fetched = provider.fetch_products(url, store_id)
    logger.info(fetched)


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--url", type=str)
    argparser.add_argument("--store_id", type=str)
    argparser.add_argument("--api", type=str, default=DEFAULT_API_BASE_URL)
    argparser.add_argument("--proxy", type=str, default=None)
    args = argparser.parse_args()

    main(args.url, args.store_id, args.api, args.proxy)
