from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.service import AuthService
from src.database import get_async_session


def get_auth_service(session: AsyncSession = Depends(get_async_session)) -> AuthService:
    return AuthService(session)
