from typing import Any
from urllib.parse import urljoin

from fastapi import FastAPI

from config import settings


def url_path_for(app: FastAPI, name: str, **path_params: Any) -> str:
    return urljoin(settings.server_url, app.url_path_for(name, **path_params))
