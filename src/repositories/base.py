from abc import ABC, abstractmethod

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.models.auth import Token, User


class AbstractRepository(ABC):

    @abstractmethod
    def get_user_or_none(self, email: str) -> [User | None]:
        pass

    @abstractmethod
    def get_user_by_token(self, token: str) -> [User | None]:
        pass


class CreateUser:
    async def create_user(self, user: User) -> User:
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user


class BaseRepository(AbstractRepository):

    async def get_user_by_token(self, token: str) -> [User | None]:
        statement = select(Token).where(Token.access_token == token).options(
            selectinload(Token.user))
        token = await self.session.execute(statement)

        if token:
            token = token.scalar_one()
            return token.user
        else:
            return None

    async def get_user_or_none(self, email: str) -> [User | None]:
        statement = select(User).where(User.email == email)
        user = await self.session.execute(statement)
        return user.scalar_one_or_none()
