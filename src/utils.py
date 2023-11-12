from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette import status

from src.database import get_async_session
from src.models import Token, User


class BaseCrud:
    session: AsyncSession

    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    async def get_user_by_token(self, token: str):
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

    def send_email(self, email: str):
        raise NotImplementedError()

    async def get_user_or_none(self, email: str) -> [User | None]:
        statement = select(User).where(User.email == email)
        db_user = await self.session.execute(statement)
        db_user = db_user.scalar_one_or_none()
        return db_user


class BaseService:
    base_crud = BaseCrud

    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.base_crud = BaseCrud(session)

    async def get_user_by_token(self, token: str) -> User:
        return await self.base_crud.get_user_by_token(token=token)

    async def get_user_or_none(self, email: str) -> [User | None]:
        return await self.base_crud.get_user_or_none(email=email)
