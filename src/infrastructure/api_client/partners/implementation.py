import asyncio
import re

import aiohttp

from src.infrastructure.api_client.partners.interface import AbstractAPIClient


class Client(AbstractAPIClient):

    def __init__(self, session):
        self.session = session

    async def _fetch_status(self, url: str, session: aiohttp.ClientSession):
        async with session.get(url) as response:
            text = await response.text()
            res = re.findall(r"<label>status: <b>\d{3}</b></label>", text)
            status_code = int(res[0].rstrip("</b></label>").lstrip("<label>status: <b>"))
            return status_code == 200

    async def execute(self, dto):
        base_url = "https://htmlweb.ru/api.php?obj=validator"

        urls = [
            f"{base_url}&m=kpp&kpp={dto.trrc}",
            f"{base_url}&m=bic&bic={dto.bic}",
            f"{base_url}&m=inn&inn={dto.tin}",
            f"{base_url}&m=phone&phone={dto.mobile}",
        ]

        async with self.session() as session:
            res = await asyncio.gather(*(self._fetch_status(url, session) for url in urls))
            return all(res)
