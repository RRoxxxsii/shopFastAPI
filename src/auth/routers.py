from fastapi import APIRouter, Depends

from src.auth.schemas import User as UserSchema
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session

router = APIRouter(prefix='/users', tags=['users'])


@router.post('/sign-up/')
async def register(user: UserSchema, session: AsyncSession = Depends(get_async_session)):
    pw = user.password1

