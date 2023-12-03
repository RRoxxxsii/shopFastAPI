import uuid
from typing import Type

from src.dto.auth import TokenDTO, UserDTO
from src.exceptions.user import PasswordIsNotCorrect, UserExists, UserNotFound
from src.models.auth import Token, User
from src.repositories.base import AbstractRepository
from src.repositories.user import AbstractUserRepository
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
        dto = UserDTO(
            email=dto.email, hashed_password=hashed_password, name=dto.name, surname=dto.surname
        )
        return await self.user_repo.create(dto=dto)

    async def execute(self, dto):
        if await self._check_if_user_exists(email=dto.email):
            raise UserExists('User with this email already exists')
        password = self._hash_password(dto.password1)
        user = await self._create_user(dto, password)
        return user


class CreateTokenService:

    def __init__(
            self, user_repo: Type[AbstractUserRepository],
            token_repo: Type[AbstractRepository],
            pwd: Type[PwdAbstract]
    ) -> None:
        self.user_repo: AbstractUserRepository = user_repo()
        self.token_repo: AbstractRepository = token_repo()
        self.pwd: PwdAbstract = pwd()

    def _check_password(self, password: str, hashed_password: str) -> bool:
        return self.pwd.check_password(password, hashed_password)

    async def _get_user_or_none(self, email: str) -> User | None:
        return await self.user_repo.get_user_by_email(email)

    async def _create_token(self, token: str, user_id: int) -> Token:
        dto = TokenDTO(access_token=token, user_id=user_id)
        return await self.token_repo.create(dto)

    async def execute(self, dto):
        user = await self._get_user_or_none(dto.email)
        if not user:
            raise UserNotFound('User with provided email does not exist')
        password = self._check_password(dto.password, user.hashed_password)
        if not password:
            raise PasswordIsNotCorrect('Password you provided is not correct')
        token = await self._create_token(token=str(uuid.uuid4()), user_id=user.id)
        return token
