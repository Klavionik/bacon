import json
from typing import Tuple
from urllib.parse import unquote

import httpx
from loguru import logger

USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/104.0.0.0 Safari/537.36"
)


class PerekrestokClient:
    def __init__(self, base_url: str, proxies: str | None):
        self.base_url = base_url
        self.token = None
        self.proxies = proxies
        self._client: httpx.Client | None = None

    def __enter__(self):
        self._client = httpx.Client(
            headers={"User-Agent": USER_AGENT}, timeout=30.0, proxies=self.proxies
        )

        token = self._fetch_token()
        self._set_token(token)
        self._client.base_url = self.base_url
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._client.close()
        self._client = None

    def get_location_coordinates(self, location: str) -> Tuple[float, float] | None:
        response = self._client.get("/geocoder/suggests", params={"search": location})
        data = response.json()
        response.raise_for_status()
        items = data["content"]["items"]

        if not items:
            return
        return items[0]["location"]["coordinates"]

    def get_stores_by_coordinates(self, coordinates: Tuple[float, float]) -> list:
        long, lat = coordinates
        params = {
            "orderBy": "distance",
            "orderDirection": "asc",
            "lat": lat,
            "lng": long,
            "page": 1,
            "perPage": 10,
        }
        response = self._client.get("/shop", params=params)
        data = response.json()
        response.raise_for_status()
        return data["content"]["items"]

    def fetch_product_data(self, item_plu: int) -> dict | None:
        url = f"catalog/product/plu{item_plu}"
        response = self._client.get(url)
        response.raise_for_status()
        return response.json()

    def set_store(self, store_id: str):
        url = "delivery/mode/pickup/%s" % store_id
        response = self._client.put(url)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def _extract_api_token(session_cookie: str) -> str:
        try:
            return json.loads(unquote(session_cookie).lstrip("j:"))["accessToken"]
        except Exception as exc:
            logger.error("Cannot extract API token with following error: %s", exc)
            raise exc

    def _fetch_token(self) -> str:
        response = self._client.get("https://www.perekrestok.ru")
        response.raise_for_status()

        session_cookie = response.cookies.get("session")

        if not session_cookie:
            logger.critical(
                f"No session cookie found in Perekrestok response. "
                f"Cookies present: {response.cookies}"
            )

        api_token = self._extract_api_token(session_cookie)
        return api_token

    def _set_token(self, token: str):
        self._client.headers = {"Authorization": f"Bearer {token}"}
