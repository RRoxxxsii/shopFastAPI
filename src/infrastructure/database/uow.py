from abc import ABC, abstractmethod

from src.infrastructure.database.repositories import (
    AbstractPartnerRepository, AbstractTokenRepository, AbstractUserRepository,
    PartnerRepository, TokenRepository, UserRepository)


class AbstractUnitOfWork(ABC):
    user_repo: AbstractUserRepository
    partner_repo: AbstractPartnerRepository
    token_repo: AbstractTokenRepository

    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, *args):
        raise NotImplementedError

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError


class UnitOfWork(AbstractUnitOfWork):
    def __init__(self, session):
        self.session_factory = session

    async def __aenter__(self):
        self.session = self.session_factory()

        self.user_repo = UserRepository(self.session)
        self.partner_repo = PartnerRepository(self.session)
        self.token_repo = TokenRepository(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
