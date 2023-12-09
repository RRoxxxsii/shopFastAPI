from abc import ABC, abstractmethod

from src.infrastructure.database.models.partner import Partner
from src.infrastructure.database.repositories.user.interface import \
    AbstractUserRepository


class AbstractPartnerRepository(AbstractUserRepository, ABC):

    @abstractmethod
    async def get_partner_or_none(self, dto) -> Partner | None:
        raise NotImplementedError
