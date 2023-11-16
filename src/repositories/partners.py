from fastapi import Depends
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.models.partners import Seller
from src.repositories.base import BaseRepository, CreateUser


class PartnerRepository(BaseRepository, CreateUser):

    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    async def get_seller_or_none(self, tin: str, an: str, company_name: str, mobile: str) -> [Seller | None]:
        statement = select(Seller).where(
            or_(
                Seller.tin == tin,
                Seller.an == an,
                Seller.company_name == company_name,
                Seller.mobile == mobile)
        )

        query = await self.session.execute(statement)
        return query.scalar_one_or_none()

    async def create_seller(self, seller: Seller) -> Seller:
        self.session.add(seller)
        await self.session.commit()
        await self.session.refresh(seller)
        return seller
