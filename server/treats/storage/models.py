from sqlalchemy import UniqueConstraint, MetaData
from sqlalchemy.orm import declarative_base, relationship

from storage.utils import (
    CharField,
    IntegerField,
    BooleanField,
    FloatField,
    DateTimeField,
    JSONField,
    ForeignKeyField,
    CascadeAction,
)

metadata = MetaData()


class Base:
    id = IntegerField(primary_key=True)

    def __repr__(self):
        return f'<{self.__class__.__name__} id={self.id}>'


Base = declarative_base(cls=Base, metadata=metadata)


class User(Base):
    __tablename__ = 'users'

    username = CharField(max_length=64)
    language = CharField(max_length=2)
    meta = JSONField(default=dict)
    treats = relationship('Treat', back_populates='user')


class Shop(Base):
    __tablename__ = 'shops'

    name = CharField(max_length=64)
    url_rule = CharField(max_length=128)
    locations = relationship('ShopLocation', back_populates='shop')


class ShopLocation(Base):
    __tablename__ = 'shop_locations'

    name = CharField(max_length=128)
    address = CharField(max_length=128)
    location_id = IntegerField()
    shop_id = ForeignKeyField('shops.id', ondelete=CascadeAction.CASCADE.value)
    products = relationship('Product', back_populates='shop_location')
    shop = relationship('Shop', back_populates='locations')


class Product(Base):
    __tablename__ = 'products'

    title = CharField(max_length=256)
    url = CharField(max_length=512)
    available = BooleanField()
    meta = JSONField(default=dict)
    shop_location_id = ForeignKeyField('shop_locations.id', ondelete=CascadeAction.RESTRICT.value)
    shop_location = relationship('ShopLocation', back_populates='products')
    prices = relationship('Price', back_populates='product')
    treats = relationship('Treat', back_populates='product')


class Price(Base):
    __tablename__ = 'prices'

    price = FloatField()
    old_price = FloatField(nullable=True)
    created_at = DateTimeField(auto_add_now=True)
    product_id = ForeignKeyField('products.id', ondelete=CascadeAction.CASCADE.value)
    product = relationship('Product', back_populates='prices')


class Treat(Base):
    __tablename__ = 'treats'

    user_id = ForeignKeyField('users.id', ondelete=CascadeAction.CASCADE.value)
    product_id = ForeignKeyField('products.id', ondelete=CascadeAction.CASCADE.value)
    created_at = DateTimeField(auto_add_now=True)
    user = relationship('User', back_populates='treats')
    product = relationship('Product', back_populates='treats')

    __table_args__ = (UniqueConstraint('user_id', 'product_id'),)
