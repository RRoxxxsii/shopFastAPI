from abc import abstractmethod

from sqlalchemy import select

from src.infrastructure.database.models.auth import User
from src.infrastructure.database.repositories.base import AbstractRepository, SQLAlchemyRepository


class AbstractUserRepository(AbstractRepository):

    @abstractmethod
    def get_user_or_none(self, email: str):
        raise NotImplementedError


class UserRepository(AbstractUserRepository, SQLAlchemyRepository):
    model = User

    async def get_user_or_none(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        user = await self.session.execute(stmt)
        return user.scalar_one_or_none()
