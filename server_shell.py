#!/usr/bin/env python3

from ptpython import embed
from core.storage import users, products, treats, prices, shops
from server.main import engine
from asdf import codes
import sqlalchemy as sa  # noqa


def configure(repl):
    repl.show_signature = True
    repl.use_code_colorscheme('monokai')
    repl.color_depth = 'DEPTH_24_BIT'
    repl.insert_blank_line_after_output = False
    repl.complete_while_typing = False
    repl.confirm_exit = False


user_data = dict(username='jediroman', telegram_id=435243, language_code='ru')
shop_data = dict(name='Перекресток', link_pattern='https://perekrestok.ru')
product_data = dict(title='чипсеки', url='https://www.perekrestok.ru/cat', shop_id=1)
price_data = dict(price=120, product_id=1)
treat_data = dict(product_id=1, user_id=1)


async def puk():
    async with engine.connect() as conn:
        async with conn.begin():
            await conn.execute(users.insert(), user_data)
            await conn.execute(shops.insert(), shop_data)
            await conn.execute(products.insert(), product_data)
            await conn.execute(prices.insert(), price_data)
            await conn.execute(treats.insert(), treat_data)


embed(globals(), locals(), configure)
