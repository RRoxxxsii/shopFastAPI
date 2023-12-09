from abc import ABC, abstractmethod

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


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
    async def create(self, dto):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_all(self):
        stmt = select(self.model)
        res = await self.session.execute(stmt)
        return res.all()

    async def get_by_id(self, pk: int) -> model:
        stmt = select(self.model).where(self.model.id == int)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def create(self, **kwargs):
        obj = self.model(**kwargs)
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj
