from abc import ABC, abstractmethod

from src.models.auth import User


class AbstractService(ABC):

    @abstractmethod
    def get_user_or_none(self, email: str) -> [User | None]:
        pass

    @abstractmethod
    def get_user_by_token(self, token: str) -> [User | None]:
        pass


class BaseService(AbstractService):

    async def get_user_by_token(self, token: str) -> [User | None]:
        return await self.repository.get_user_by_token(token=token)

    async def get_user_or_none(self, email: str) -> [User | None]:
        return await self.repository.get_user_or_none(email=email)
