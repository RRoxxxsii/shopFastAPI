from abc import ABC, abstractmethod

from src.models.auth import User
from src.secure import pwd_context


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


class CreateUser:

    async def create_user(self, user_schema, hashed_password: str) -> User:
        user = User(
            name=user_schema.name,
            surname=user_schema.surname,
            email=user_schema.email,
            hashed_password=hashed_password
        )
        return await self.repository.create_user(user=user)

    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)
