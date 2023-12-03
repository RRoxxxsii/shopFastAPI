import asyncio
from abc import ABC, abstractmethod

from src.api.partners.validate import APICall


class AbstractClient(ABC):

    @abstractmethod
    async def call(self, *args) -> bool:
        raise NotImplementedError


class Client(AbstractClient):

    async def call(self, *args) -> bool:
        res = await asyncio.gather(*(APICall.validate(url) for url in args))
        return all(res)
