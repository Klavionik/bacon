import argparse

from loguru import logger

from .config import config
from .scraper import PerekrestokScraper


def main(url: str, store_id: int):
    scraper = PerekrestokScraper(config)
    fetched = scraper.fetch(url, store_id)
    logger.info(fetched)


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--url", type=str)
    argparser.add_argument("--store_id", type=int)
    args = argparser.parse_args()

    main(args.url, args.store_id)
