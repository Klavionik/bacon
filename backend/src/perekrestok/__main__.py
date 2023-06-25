import argparse
import asyncio

from perekrestok.parser import PerekrestokParser


async def main(url: str, shop_location_external_id: int):
    parser = PerekrestokParser()
    fetched = await parser.fetch_products(url, shop_location_external_id)
    print(fetched)


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("url", type=str)
    argparser.add_argument("shop_id", type=int)
    args = argparser.parse_args()

    asyncio.run(main(args.url, args.shop_id))
