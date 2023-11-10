import asyncio
import re

from src.http_session import HTTPSessionManager
from src.partners.crud import UpgradePartnerCrud


class APICall:
    @staticmethod
    async def validate(url: str):
        session = HTTPSessionManager.get_session()
        async with session.get(url, ssl=False) as response:
            text = await response.text()
            res = re.findall(r'<label>status: <b>\d{3}</b></label>', text)
            status_code = int(res[0].rstrip('</b></label>').lstrip('<label>status: <b>'))
            return status_code == 200


class ValidateCredentials(APICall):
    pass


class PartnerService(UpgradePartnerCrud, ValidateCredentials):
    async def validate_data(self):
        trrc, bic, tin, mobile = await asyncio.gather(
            self.validate(f'https://htmlweb.ru/api.php?obj=validator&m=kpp&kpp={self.seller.trrc}'),
            self.validate(f'https://htmlweb.ru/api.php?obj=validator&m=bic&bic={self.seller.bic}'),
            self.validate(f'https://htmlweb.ru/api.php?obj=validator&m=inn&inn={self.seller.tin}'),
            self.validate(f'https://htmlweb.ru/api.php?obj=validator&m=phone&phone={self.seller.mobile}')
        )
        return all((trrc, bic, tin, mobile))


class UpgradePartnerService(PartnerService):
    pass


class BecomePartnerService(PartnerService):
    pass
