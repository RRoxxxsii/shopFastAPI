from sqlalchemy import or_, select

from src.infrastructure.database.models.partner import Partner
from src.infrastructure.database.repositories.partner.interface import (
    AbstractPartnerRepository,
)
from src.infrastructure.database.repositories.user.implementation import UserRepository


class PartnerRepository(AbstractPartnerRepository, UserRepository):
    model = Partner

    async def get_partner_or_none(self, dto) -> Partner | None:
        stmt = select(Partner).where(
            or_(
                Partner.tin == dto.tin,
                Partner.an == dto.an,
                Partner.company_name == dto.company_name,
                Partner.mobile == dto.mobile,
            )
        )
        result = await self.session.execute(stmt)
        partner = result.scalar_one_or_none()
        return partner
