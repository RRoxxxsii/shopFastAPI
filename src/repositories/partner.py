from abc import abstractmethod

from sqlalchemy import or_, select

from src.database import async_session_maker
from src.models.partners import Seller
from src.repositories.user import AbstractUserRepository, UserRepository


class AbstractPartnerRepository(AbstractUserRepository):

    @abstractmethod
    async def get_partner_or_none(self, dto) -> Seller | None:
        raise NotImplementedError


class PartnerRepository(AbstractPartnerRepository, UserRepository):
    model = Seller

    async def get_partner_or_none(self, dto) -> Seller | None:
        async with async_session_maker() as session:
            stmt = select(Seller).where(
                or_(
                    Seller.tin == dto.tin,
                    Seller.an == dto.an,
                    Seller.company_name == dto.company_name,
                    Seller.mobile == dto.mobile)
            )
            result = await session.execute(stmt)
            seller = result.scalar_one_or_none()
            return seller
