from abc import abstractmethod, ABC
from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.database import get_async_session
from src.models.auth import Token, User
from src.secure import pwd_context, apikey_scheme


class PwdAbstract(ABC):

    @abstractmethod
    def check_password(self, password: str, hashed_password: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def hash_password(self, password: str) -> str:
        raise NotImplementedError


class PwdImpl(PwdAbstract):

    def check_password(self, password: str, hashed_password: str) -> bool:
        return pwd_context.verify(password, hashed_password)

    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)


async def get_current_user(
        access_token: Annotated[str, Depends(apikey_scheme)],
        session: AsyncSession = Depends(get_async_session)
) -> User | None:

    stmt = select(Token).where(Token.access_token == access_token).options(selectinload(Token.user))
    token = await session.execute(stmt)

    if token:
        token = token.scalar_one()
        return token.user
    else:
        return None
