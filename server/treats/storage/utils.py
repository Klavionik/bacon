from enum import Enum
from typing import Callable

from sqlalchemy import Column, Integer, Float, String, DateTime, JSON, func, ForeignKey, Boolean
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


class CascadeAction(str, Enum):
    CASCADE = 'CASCADE'
    RESTRICT = 'RESTRICT'


class CharField:
    def __new__(cls, *, max_length: int, nullable=False, **kwargs):
        return Column(String(max_length), nullable=nullable, **kwargs)


class IntegerField:
    def __new__(cls, *, nullable=False, **kwargs):
        return Column(Integer, nullable=nullable, **kwargs)


class FloatField:
    def __new__(cls, *, precision=None, nullable=False, **kwargs):
        return Column(Float(precision), nullable=nullable, **kwargs)


class DateTimeField:
    def __new__(cls, *, nullable=False, auto_add_now=False, **kwargs):
        server_default = func.now() if auto_add_now and not nullable else None
        return Column(DateTime(timezone=True), nullable=nullable, server_default=server_default, **kwargs)


class JSONField:
    def __new__(cls, *, nullable=False, **kwargs):
        return Column(JSON, nullable=nullable, **kwargs)


class ForeignKeyField:
    def __new__(cls, reference: str, ondelete: CascadeAction, **kwargs):
        return Column(Integer, ForeignKey(reference, ondelete=ondelete), **kwargs)


class BooleanField:
    def __new__(cls, default: bool = False, nullable=False, **kwargs):
        return Column(Boolean, default=default, nullable=nullable, **kwargs)


def create_db_engine(db_uri: str, echo: bool = False) -> AsyncEngine:
    return create_async_engine(db_uri, echo=echo)


def create_db_session(engine: AsyncEngine) -> Callable[[], AsyncSession]:
    return sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
