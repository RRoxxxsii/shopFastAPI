from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.partners.schemas import SellerIn
from src.partners.service import BecomePartnerService


def become_partner_service(
        seller: SellerIn,
        session: AsyncSession = Depends(get_async_session)
) -> BecomePartnerService:
    return BecomePartnerService(session=session, seller=seller)
