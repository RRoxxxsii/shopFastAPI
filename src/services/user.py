from typing import Type

from src.exceptions.user import UserExists
from src.models.auth import User
from src.repositories.base import AbstractRepository
from src.repositories.user import AbstractUserRepository
from src.schemas.auth import UserSchema
from src.secure.pwd import PwdAbstract


class CreateUserService:

    def __init__(self, user_repo: Type[AbstractUserRepository], pwd: Type[PwdAbstract]):
        self.user_repo = user_repo()
        self.pwd = pwd()

    def _hash_password(self, password: str) -> str:
        return self.pwd.hash_password(password)

    async def _check_if_user_exists(self, email: str) -> User | None:
        return await self.user_repo.get_user_by_email(email=email)

    async def _create_user(self, dto, hashed_password: str) -> User:
        dto = UserSchema(
            email=dto.email, hashed_password=hashed_password, name=dto.name, surname=dto.surname
        )
        return await self.user_repo.create(dto=dto)

    async def execute(self, dto):
        if await self._check_if_user_exists(email=dto.email):
            raise UserExists('Пользователь с таким адресом существует')
        password = self._hash_password(dto.password1)
        user = await self._create_user(dto, password)
        return user
