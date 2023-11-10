from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.partners.schemas import SellerIn
from src.partners.service import UpgradePartnerService


def upgrade_partner_service(
        seller: SellerIn,
        session: AsyncSession = Depends(get_async_session)
) -> UpgradePartnerService:
    return UpgradePartnerService(session=session, seller=seller)
