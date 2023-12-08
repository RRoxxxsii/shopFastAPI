import uuid
from typing import Type

from src.database.uow import UnitOfWork
from src.dto.auth import TokenDTO
from src.exceptions.user import PasswordIsNotCorrect, UserExists, UserNotFound
from src.models.auth import Token, User
from src.repositories.base import AbstractRepository
from src.repositories.user import AbstractUserRepository
from src.secure.pwd import check_password


class BaseUseCase:

    def __init__(self, uow: UnitOfWork) -> None:
        self.uow: UnitOfWork = uow


class UserUseCase(BaseUseCase):

    def __init__(self, uow: UnitOfWork) -> None:
        super().__init__(uow)


class TokenUseCase(BaseUseCase):

    def __init__(self, uow: UnitOfWork) -> None:
        super().__init__(uow)


class CreateUser(UserUseCase):

    async def __call__(self, user_dto) -> User:
        async with self.uow:
            if await self.uow.user_repo.get_user_or_none(user_dto.email):
                raise UserExists('User with this email already exists')
            user = await self.uow.user_repo.create(
                hashed_password=user_dto.password1,
                **user_dto.model_dump(include={'name', 'surname', 'email'})
            )
            await self.uow.commit()
            return user


class CreateToken(TokenUseCase):

    async def __call__(self, user_dto) -> Token:
        async with self.uow:
            user = await self.uow.user_repo.get_user_or_none(user_dto.email)
            if not user:
                raise UserNotFound('User with provided email does not exist')
            password = check_password(user_dto.password, user.hashed_password)
            if not password:
                raise PasswordIsNotCorrect('Password you provided is not correct')
            token = await self.uow.token_repo.create(access_token=str(uuid.uuid4()), user_id=user.id)
            return token


class CreateUserService:

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def _create_user(self, user_dto):
        return await CreateUser(self.uow)(user_dto)

    async def execute(self, user_dto):
        return await self._create_user(user_dto)


class CreateTokenService:

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def _create_token(self, user_dto):
        return await CreateToken(self.uow)(user_dto)

    async def execute(self, user_dto):
        return await self._create_token(user_dto)

# class CreateTokenService:
#
#     def __init__(
#             self, user_repo: Type[AbstractUserRepository],
#             token_repo: Type[AbstractRepository],
#     ) -> None:
#         self.user_repo: AbstractUserRepository = user_repo()
#         self.token_repo: AbstractRepository = token_repo()
#
#     def _check_password(self, password: str, hashed_password: str) -> bool:
#         return self.pwd.check_password(password, hashed_password)
#
#     async def _get_user_or_none(self, email: str) -> User | None:
#         return await self.user_repo.get_user_by_email(email)
#
#     async def _create_token(self, token: str, user_id: int) -> Token:
#         dto = TokenDTO(access_token=token, user_id=user_id)
#         return await self.token_repo.create(dto)
#
#     async def execute(self, dto):
#         user = await self._get_user_or_none(dto.email)
#         if not user:
#             raise UserNotFound('User with provided email does not exist')
#         password = self._check_password(dto.password, user.hashed_password)
#         if not password:
#             raise PasswordIsNotCorrect('Password you provided is not correct')
#         token = await self._create_token(token=str(uuid.uuid4()), user_id=user.id)
#         return token
