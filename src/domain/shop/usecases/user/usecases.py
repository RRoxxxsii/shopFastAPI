import uuid

from src.domain.shop.dto.auth import AuthDTO, UserDTO
from src.domain.shop.exceptions.user import (
    PasswordIsNotCorrect,
    UserExists,
    UserNotFound,
)
from src.domain.shop.usecases.user.base import TokenUseCase, UserUseCase
from src.infrastructure.database.models.auth import Token, User
from src.infrastructure.secure.pwd import check_password


class CreateUser(UserUseCase):
    async def __call__(self, user_dto: UserDTO) -> User:
        async with self.uow:
            if await self.uow.user_repo.get_user_or_none(user_dto.email):
                raise UserExists("User with this email already exists")
            user = await self.uow.user_repo.create(
                hashed_password=user_dto.password1, **user_dto.model_dump(include={"name", "surname", "email"})
            )
            await self.uow.commit()
            return user


class CreateToken(TokenUseCase):
    async def __call__(self, user_dto: AuthDTO) -> Token:
        async with self.uow:
            user = await self.uow.user_repo.get_user_or_none(user_dto.email)
            if not user:
                raise UserNotFound("User with provided email does not exist")
            password = check_password(user_dto.password, user.hashed_password)
            if not password:
                raise PasswordIsNotCorrect("Password you provided is not correct")
            token = await self.uow.token_repo.create(access_token=str(uuid.uuid4()), user_id=user.id)
            return token
