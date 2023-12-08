from typing import Type

from src.api.partners.client import AbstractAPIClient
from src.database.uow import UnitOfWork
from src.exceptions.partner import DataNotValid, SellerExists
from src.exceptions.user import UserExists
from src.models.partners import Seller
from src.secure.pwd import hash_password


class BaseUseCase:

    def __init__(self, uow: UnitOfWork) -> None:
        self.uow: UnitOfWork = uow


class SellerUseCase(BaseUseCase):
    def __init__(self, uow: UnitOfWork, api_client: Type[AbstractAPIClient]):
        super().__init__(uow)
        self.api_client: Type[AbstractAPIClient] = api_client


class CreateSellerUserDoesNotExists(SellerUseCase):

    async def __call__(self, partner_dto, user_dto) -> Seller:
        async with self.uow:
            if await self.uow.user_repo.get_user_or_none(user_dto.email):
                raise UserExists('User with this credentials already exists')
            if await self.uow.partner_repo.get_partner_or_none(partner_dto):
                raise SellerExists('Seller with this credentials already exists')
            if not await self.api_client.call(partner_dto):
                raise DataNotValid('Data you provided is not valid')
            user = await self.uow.user_repo.create(
                hashed_password=hash_password(user_dto.password1), **user_dto.model_dump(
                    include={'name', 'surname', 'email'},
                )
            )
            seller = await self.uow.partner_repo.create(user_id=user.id, **partner_dto.model_dump())
            await self.uow.commit()
            return seller


class CreateSellerUserExists(SellerUseCase):

    async def __call__(self, dto) -> Seller:
        async with self.uow:
            if await self.uow.partner_repo.get_partner_or_none(dto):
                raise SellerExists('Seller with this credentials already exists')
            if not await self.api_client.call(dto):
                raise DataNotValid('Data you provided is not valid')
            seller = await self.uow.partner_repo.create(**dto.model_dump())
            await self.uow.commit()
            return seller


class CreatePartnerUserExistsService:
    def __init__(
            self,
            api_client: Type[AbstractAPIClient],
            uow: UnitOfWork
    ):
        self.api_client: Type[AbstractAPIClient] = api_client
        self.uow: UnitOfWork = uow

    async def _create_seller(self, dto):
        return await CreateSellerUserExists(self.uow, self.api_client)(dto)

    async def execute(self, dto) -> Seller:
        seller = await self._create_seller(dto)
        return seller


class CreatePartnerUserDoesNotExistsService:
    def __init__(
            self,
            api_client: Type[AbstractAPIClient],
            uow: UnitOfWork
    ):
        self.api_client: Type[AbstractAPIClient] = api_client
        self.uow: UnitOfWork = uow

    async def _create_seller(self, partner_dto, user_dto):
        return await CreateSellerUserDoesNotExists(self.uow, self.api_client)(partner_dto, user_dto)

    async def execute(self, partner_dto, user_dto) -> Seller:
        seller = await self._create_seller(partner_dto, user_dto)
        return seller
