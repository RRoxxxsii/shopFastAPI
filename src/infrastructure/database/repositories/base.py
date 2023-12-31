from abc import ABC, abstractmethod

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.base import AbstractModel


class AbstractRepository(ABC):
    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    async def find_all(self):
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, pk: int):
        raise NotImplementedError

    @abstractmethod
    async def create(self, **kwargs):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model: type[AbstractModel]

    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_all(self):
        stmt = select(self.model)
        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def get_by_id(self, pk: int) -> AbstractModel | None:
        stmt = select(self.model).where(self.model.id == pk)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def create(self, **kwargs) -> AbstractModel:
        obj = self.model(**kwargs)
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj
