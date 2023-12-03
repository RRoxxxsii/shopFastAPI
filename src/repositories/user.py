from abc import ABC, abstractmethod

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session, async_session_maker
from src.models.auth import User, Token
from src.repositories.base import AbstractRepository, SQLAlchemyRepository


class AbstractUserRepository(AbstractRepository):

    @abstractmethod
    def get_user_by_email(self, email: str):
        raise NotImplementedError


class UserRepository(AbstractUserRepository, SQLAlchemyRepository):
    model = User

    async def get_user_by_email(self, email: str) -> User | None:
        async with async_session_maker() as session:
            stmt = select(User).where(User.email == email)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()
