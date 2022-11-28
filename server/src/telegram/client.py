from urllib.parse import urljoin

import httpx


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

    async def send_message(self, chat_id: int, text: str, *, html: bool = False) -> dict:
        data = {'chat_id': chat_id, 'text': text}

        if html:
            data.update(parse_mode='HTML')
        return await self.request('POST', 'sendMessage', data)

    async def request(self, method: str, url: str, data: dict = None):
        async with httpx.AsyncClient(base_url=self.base_url) as client:
            response = await client.request(method, url, data=data)

        data = response.json()
        data_is_ok = data.get('ok')

        if not data_is_ok:
            raise RuntimeError(f'Request to {response.request.url} returned an error: {data}')
        return data.get('result')
