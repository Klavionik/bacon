import functools
import importlib
import inspect


def is_scraper(obj: object):
    return inspect.isclass(obj) and obj.__name__.lower().endswith("scraper")


@functools.cache
def list_scrapers(scrapers_dir: str):
    scrapers = []
    scrapers_pkg = importlib.import_module(scrapers_dir)
    pkg_attrs = dir(scrapers_pkg)

    for attr in pkg_attrs:
        obj = getattr(scrapers_pkg, attr)

        if is_scraper(obj):
            scrapers.append(f"{scrapers_dir}.{obj.__name__}")

    return scrapers
