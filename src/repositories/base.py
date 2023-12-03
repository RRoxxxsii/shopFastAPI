from abc import ABC, abstractmethod

from sqlalchemy import select

from src.database import async_session_maker


class AbstractRepository(ABC):

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

    async def find_all(self):
        async with async_session_maker() as session:
            stmt = select(self.model)
            res = await session.execute(stmt)
            return res.all()

    async def get_by_id(self, pk: int) -> model:
        async with async_session_maker() as session:
            stmt = select(self.model).where(self.model.id == int)
            res = await session.execute(stmt)
            return res.scalar_one_or_none()

    async def create(self, dto):
        async with async_session_maker() as session:
            obj = self.model(**dto.model_dump())
            session.add(obj)
            await session.commit()
            await session.refresh(obj)
            return obj
