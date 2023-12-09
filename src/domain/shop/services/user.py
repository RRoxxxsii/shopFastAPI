from src.infrastructure.database.uow import AbstractUnitOfWork
from src.domain.shop.dto.auth import AuthDTO, CreateUserDTO
from src.domain.shop.usecases.user.usecases import CreateUser, CreateToken


class CreateUserService:

    def __init__(self, uow: AbstractUnitOfWork):
        self.uow: AbstractUnitOfWork = uow

    async def _create_user(self, user_dto: CreateUserDTO):
        return await CreateUser(self.uow)(user_dto)

    async def execute(self, user_dto: CreateUserDTO):
        return await self._create_user(user_dto)


class CreateTokenService:

    def __init__(self, uow: AbstractUnitOfWork):
        self.uow: AbstractUnitOfWork = uow

    async def _create_token(self, user_dto: AuthDTO):
        return await CreateToken(self.uow)(user_dto)

    async def execute(self, user_dto: AuthDTO):
        return await self._create_token(user_dto)
