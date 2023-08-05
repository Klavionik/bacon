import functools
import importlib
import inspect
import pathlib

from web.scraping.providers.base import BaseProvider


def is_provider(obj: type):
    return inspect.isclass(obj) and issubclass(obj, BaseProvider) and not inspect.isabstract(obj)


@functools.cache
def list_scrapers(providers_dir: pathlib.Path):
    scrapers = []
    scrapers_pkg = importlib.import_module(str(providers_dir))
    pkg_attrs = dir(scrapers_pkg)

    for attr in pkg_attrs:
        obj = getattr(scrapers_pkg, attr)

        if is_provider(obj):
            scrapers.append(f"{providers_dir}.{obj.__name__}")

    return scrapers
