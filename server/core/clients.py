import json
import logging
from typing import Tuple
from urllib.parse import urljoin, unquote

import httpx

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'

logging.basicConfig()
log = logging.getLogger(__name__)


class TelegramClient:
    def __init__(self, base_url: str, token: str, server_url: str, server_secret: str):
        self.base_url = base_url % {'token': token}
        self.server_url = server_url
        self.server_secret = server_secret

    async def get_webhook_info(self) -> dict:
        return await self.request('GET', 'getWebhookInfo')

    async def set_webhook(self, webhook_route: str) -> dict:
        data = {'url': urljoin(self.server_url, webhook_route), 'secret_token': self.server_secret}
        return await self.request('POST', 'setWebhook', data)

    async def send_message(self, chat_id: int, text: str) -> dict:
        data = {'chat_id': chat_id, 'text': text}
        return await self.request('POST', 'sendMessage', data)

    async def request(self, method: str, url: str, data: dict = None):
        async with httpx.AsyncClient(base_url=self.base_url) as client:
            response = await client.request(method, url, data=data)

        data = response.json()
        data_is_ok = data.get('ok')

        if not data_is_ok:
            raise RuntimeError(f'Request to {response.request.url} returned an error: {data}')
        return data.get('result')


class PerekrestokClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.token = None
        self.client: httpx.AsyncClient | None = None

    async def __aenter__(self):
        self.client = httpx.AsyncClient(
            headers={'User-Agent': USER_AGENT},
            timeout=30.0
        )

        token = await self._fetch_token()
        self._set_token(token)
        self.client.base_url = self.base_url
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
        self.client = None

    async def get_location_coordinates(self, location: str) -> Tuple[float, float]:
        response = await self.client.get('/geocoder/suggests', params={'search': location})
        data = response.json()
        response.raise_for_status()
        return data['content']['items'][0]['location']['coordinates']

    async def get_shop_by_coordinates(self, coordinates: Tuple[float, float]) -> Tuple[int, str, str]:
        long, lat = coordinates
        params = {
            'orderBy': 'distance',
            'orderDirection': 'asc',
            'lat': lat,
            'lng': long,
            'page': 1,
            'perPage': 1
        }
        response = await self.client.get('/shop', params=params)
        data = response.json()
        response.raise_for_status()
        [shop] = data['content']['items']
        title = shop['title']
        shop_id = shop['id']
        address = shop['address']
        return shop_id, title, address

    async def fetch_product_data(self, item_plu: int) -> dict | None:
        url = f'catalog/product/plu{item_plu}'
        response = await self.client.get(url)
        response.raise_for_status()
        return response.json()

    async def set_shop(self, shop_id: int):
        url = 'delivery/mode/pickup/%s' % shop_id
        response = await self.client.put(url)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def _extract_api_token(session_cookie: str) -> str:
        try:
            return json.loads(unquote(session_cookie).lstrip('j:'))['accessToken']
        except Exception as exc:
            log.error('Cannot extract API token with following error: %s', exc)

    async def _fetch_token(self) -> str:
        response = await self.client.get('https://www.perekrestok.ru')
        response.raise_for_status()

        session_cookie = response.cookies.get('session')
        api_token = self._extract_api_token(session_cookie)
        return api_token

    def _set_token(self, token: str):
        self.client.headers = {'Authorization': f'Bearer {token}'}
