from abc import ABC, abstractmethod

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from starlette import status

from src.models.auth import User, Token


class AbstractRepository(ABC):

    @abstractmethod
    def get_user_or_none(self, email: str) -> [User | None]:
        pass

    @abstractmethod
    def get_user_by_token(self, token: str) -> [User | None]:
        pass


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
