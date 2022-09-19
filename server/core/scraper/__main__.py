import argparse
import asyncio

from .parsers import get_parser_by_url
from core.clients import PerekrestokClient


async def main(url: str, shop_location_id: str):
    context = dict(items=[url.rsplit('-', maxsplit=1)[-1]], shop_location_id=shop_location_id)
    pc = PerekrestokClient('https://www.perekrestok.ru/api/customer/1.4.1.0')
    parser = get_parser_by_url(url)(pc, context)

    async for product in parser.fetch():
        print(product)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('url', type=str)
    argparser.add_argument('shop_id', type=int)
    args = argparser.parse_args()

    asyncio.run(main(args.url, args.shop_id))
