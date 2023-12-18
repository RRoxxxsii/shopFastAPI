from abc import ABC, abstractmethod


class AbstractAPIClient(ABC):
    @abstractmethod
    def __init__(self, session):
        raise NotImplementedError

    @abstractmethod
    async def _fetch_status(self, url: str, session):
        raise NotImplementedError

    @abstractmethod
    async def execute(self, dto):
        raise NotImplementedError
