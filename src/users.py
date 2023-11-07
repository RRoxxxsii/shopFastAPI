from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette import status

from src import models


async def get_user_by_token(token: str, session: AsyncSession):
    statement = select(models.Token).where(models.Token.access_token == token).options(selectinload(models.Token.user))
    token = await session.execute(statement)

    # Think about what to do when no objects found
    if token:
        token = token.scalar_one()
        return token.user
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='UNAUTHORIZED'
        )
