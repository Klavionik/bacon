from datetime import date
from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey, Float, Date, UniqueConstraint

metadata = MetaData()

users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('telegram_id', Integer, nullable=False, index=True),
    Column('username', String(256), nullable=False),
    Column('language_code', String(4), nullable=False),
)

shops = Table(
    'shops',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(128), nullable=False),
    Column('link_pattern', String(256), nullable=False),
)

products = Table(
    'products',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String(256), nullable=False),
    Column('url', String(512), nullable=False, unique=True),
    Column('shop_id', Integer, ForeignKey('shops.id'), nullable=False),
)

prices = Table(
    'prices',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('price', Float, nullable=False),
    Column('last_price', Float),
    Column('product_id', Integer, ForeignKey('products.id'), nullable=False),
    Column('created_at', Date, default=date.today, index=True)
)

treats = Table(
    'treats',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('created_at', Date, default=date.today),
    Column('product_id', Integer, ForeignKey('products.id'), nullable=False),
    Column('user_id', Integer, ForeignKey('users.id'), nullable=False),
    UniqueConstraint('product_id', 'user_id'),
)
