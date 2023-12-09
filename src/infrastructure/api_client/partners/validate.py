import re

from src.infrastructure.api_client.httpSessionManager import HTTPSessionManager


class APICall:
    @staticmethod
    async def validate(url: str):
        session = HTTPSessionManager.get_session()

        async with session.get(url, ssl=False) as response:
            text = await response.text()
            res = re.findall(r'<label>status: <b>\d{3}</b></label>', text)
            status_code = int(res[0].rstrip('</b></label>').lstrip('<label>status: <b>'))
            return status_code == 200
