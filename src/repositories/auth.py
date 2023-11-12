import uuid

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette import status

from src.database import get_async_session
from src.models.auth import User, Token


class AuthRepository:
    session: AsyncSession

    def __init__(self, session: AsyncSession = Depends(get_async_session)) -> None:
        self.session = session

    async def get_user_or_none(self, email: str) -> [User | None]:
        statement = select(User).where(User.email == email)
        user = await self.session.execute(statement)
        return user.scalar_one_or_none()

    async def get_user_by_token(self, token: str) -> [User | None]:
        statement = select(Token).where(Token.access_token == token).options(
            selectinload(Token.user))
        token = await self.session.execute(statement)

        if token:
            token = token.scalar_one_or_none()
            return token.user
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='UNAUTHORIZED'
            )

    async def create_token(self, token: Token) -> str:
        self.session.add(token)
        await self.session.commit()
        await self.session.refresh(token)
        return token.access_token

    async def create_user(self, user: User) -> User:
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
