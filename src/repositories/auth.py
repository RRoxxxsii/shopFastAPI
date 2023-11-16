from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.models.auth import Token
from src.repositories.base import BaseRepository, CreateUser


class AuthRepository(BaseRepository, CreateUser):
    session: AsyncSession

    def __init__(self, session: AsyncSession = Depends(get_async_session)) -> None:
        self.session = session

    async def create_token(self, token: Token) -> str:
        self.session.add(token)
        await self.session.commit()
        await self.session.refresh(token)
        return token.access_token

