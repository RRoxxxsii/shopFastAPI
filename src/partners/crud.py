from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Seller
from src.partners.schemas import SellerIn
from src.utils import BaseCrud


class UpgradePartnerCrud(BaseCrud):

    def __init__(self, seller: SellerIn, session: AsyncSession):
        super().__init__(session)
        self.seller = seller

    async def get_seller_exists(self) -> [Seller | None]:
        statement = select(Seller).where(
            or_(
                Seller.tin == self.seller.tin,
                Seller.an == self.seller.an,
                Seller.company_name == self.seller.company_name,
                Seller.mobile == self.seller.mobile)
        )

        query = await self.session.execute(statement)
        return query.scalar_one_or_none()

    async def create_seller(self, user):
        seller = Seller(user=user, **dict(self.seller))

        self.session.add(seller)
        await self.session.commit()
        await self.session.refresh(seller)
        return seller
