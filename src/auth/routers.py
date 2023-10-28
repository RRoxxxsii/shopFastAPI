import bcrypt
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src import models
from src.auth import schemas
from src.database import get_async_session

router = APIRouter(prefix='/users', tags=['users'])


@router.post('/sign-up/', response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
async def register(user: schemas.UserIn, session: AsyncSession = Depends(get_async_session)):
    db_user = models.User(
        name=user.name, surname=user.surname, email=user.email, hashed_password=user.password1
    )
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user
