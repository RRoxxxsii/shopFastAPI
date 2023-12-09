from src.api.partners.client import AbstractAPIClient
from src.database.uow import AbstractUnitOfWork
from src.dto.auth import CreateUserDTO
from src.dto.partner import PartnerDTO, UserPartnerDTO
from src.exceptions.partner import DataNotValid, PartnerExists
from src.exceptions.user import UserExists
from src.models.partner import Partner
from src.secure.pwd import hash_password


class BaseUseCase:

    def __init__(self, uow: AbstractUnitOfWork) -> None:
        self.uow: AbstractUnitOfWork = uow


class PartnerUseCase(BaseUseCase):
    def __init__(self, uow: AbstractUnitOfWork, api_client: AbstractAPIClient):
        super().__init__(uow)
        self.api_client: AbstractAPIClient = api_client


class CreatePartnerUserDoesNotExists(PartnerUseCase):

    async def __call__(self, partner_dto: PartnerDTO, user_dto: CreateUserDTO) -> Partner:
        async with self.uow:
            if await self.uow.user_repo.get_user_or_none(user_dto.email):
                raise UserExists('User with this credentials already exists')
            if await self.uow.partner_repo.get_partner_or_none(partner_dto):
                raise PartnerExists('Partner with this credentials already exists')
            if not await self.api_client.call(partner_dto):
                raise DataNotValid('Data you provided is not valid')
            user = await self.uow.user_repo.create(
                hashed_password=hash_password(user_dto.password1), **user_dto.model_dump(
                    include={'name', 'surname', 'email'},
                )
            )
            partner = await self.uow.partner_repo.create(user_id=user.id, **partner_dto.model_dump())
            await self.uow.commit()
            return partner


class CreatePartnerUserExists(PartnerUseCase):

    async def __call__(self, dto: UserPartnerDTO) -> Partner:
        async with self.uow:
            if await self.uow.partner_repo.get_partner_or_none(dto):
                raise PartnerExists('Partner with this credentials already exists')
            if not await self.api_client.call(dto):
                raise DataNotValid('Data you provided is not valid')
            partner = await self.uow.partner_repo.create(**dto.model_dump())
            await self.uow.commit()
            return partner


class CreatePartnerUserExistsService:
    def __init__(
            self,
            api_client: AbstractAPIClient,
            uow: AbstractUnitOfWork
    ):
        self.api_client: AbstractAPIClient = api_client
        self.uow: AbstractUnitOfWork = uow

    async def _create_partner(self, dto: UserPartnerDTO):
        return await CreatePartnerUserExists(self.uow, self.api_client)(dto)

    async def execute(self, dto: UserPartnerDTO) -> Partner:
        partner = await self._create_partner(dto)
        return partner


class CreatePartnerUserDoesNotExistsService:
    def __init__(
            self,
            api_client: AbstractAPIClient,
            uow: AbstractUnitOfWork
    ):
        self.api_client: AbstractAPIClient = api_client
        self.uow: AbstractUnitOfWork = uow

    async def _create_partner(self, partner_dto: PartnerDTO, user_dto: CreateUserDTO):
        return await CreatePartnerUserDoesNotExists(self.uow, self.api_client)(partner_dto, user_dto)

    async def execute(self, partner_dto: PartnerDTO, user_dto: CreateUserDTO) -> Partner:
        partner = await self._create_partner(partner_dto, user_dto)
        return partner
