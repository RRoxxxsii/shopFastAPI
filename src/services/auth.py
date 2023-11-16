import uuid

from fastapi import Depends

from src.models.auth import Token, User
from src.repositories.auth import AuthRepository
from src.schemas.auth import RegisterUserIn
from src.secure import pwd_context
from src.services.base import BaseService


class AuthService(BaseService):

    def __init__(self, auth_repository: AuthRepository = Depends()) -> None:
        self.repository = auth_repository

    async def create_token(self, user_id: int) -> str:
        token = Token(user_id=user_id, access_token=str(uuid.uuid4()))
        return await self.repository.create_token(token)

    async def create_user(self, user_schema: RegisterUserIn, hashed_password: str) -> User:
        user = User(
            name=user_schema.name,
            surname=user_schema.surname,
            email=user_schema.email,
            hashed_password=hashed_password
        )
        return await self.repository.create_user(user=user)

    def check_password(self, password: str, hashed_password: str) -> bool:
        return pwd_context.verify(password, hashed_password)

    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)
