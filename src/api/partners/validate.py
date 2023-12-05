import re

from src.api.httpSessionManager import HTTPSessionManager


class APICall:
    @staticmethod
    async def validate(url: str):
        session = HTTPSessionManager.get_session()

        urls = [
            'https://htmlweb.ru/api.php?obj=validator&m=kpp&kpp=',
            'https://htmlweb.ru/api.php?obj=validator&m=bic&bic=',
            'https://htmlweb.ru/api.php?obj=validator&m=inn&inn=',
            'https://htmlweb.ru/api.php?obj=validator&m=phone&phone='
        ]

        async with session.get(url, ssl=False) as response:
            text = await response.text()
            res = re.findall(r'<label>status: <b>\d{3}</b></label>', text)
            status_code = int(res[0].rstrip('</b></label>').lstrip('<label>status: <b>'))
            return status_code == 200
