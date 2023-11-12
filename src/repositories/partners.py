from fastapi import Depends, HTTPException
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette import status

from src.database import get_async_session
from src.models.auth import Token, User
from src.models.partners import Seller


class PartnerRepository:

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

    async def get_user_by_token(self, token: str) -> [User | None]:
        statement = select(Token).where(Token.access_token == token).options(
            selectinload(Token.user))
        token = await self.session.execute(statement)

        if token:
            token = token.scalar_one()
            return token.user
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='UNAUTHORIZED'
            )

    async def create_seller(self, seller: Seller) -> Seller:
        self.session.add(seller)
        await self.session.commit()
        await self.session.refresh(seller)
        return seller
