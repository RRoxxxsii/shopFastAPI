import asyncio
from abc import ABC, abstractmethod

from src.api.partners.validate import APICall


class AbstractAPIClient(ABC):

    @abstractmethod
    async def call(self, *args) -> bool:
        raise NotImplementedError


class Client(AbstractAPIClient):

    async def call(self, dto) -> bool:
        urls = [
            f'https://htmlweb.ru/api.php?obj=validator&m=kpp&kpp={dto.trrc}',
            f'https://htmlweb.ru/api.php?obj=validator&m=bic&bic={dto.bic}',
            f'https://htmlweb.ru/api.php?obj=validator&m=inn&inn={dto.tin}',
            f'https://htmlweb.ru/api.php?obj=validator&m=phone&phone={dto.mobile}'
        ]
        res = await asyncio.gather(*(APICall.validate(url) for url in urls))
        return all(res)
