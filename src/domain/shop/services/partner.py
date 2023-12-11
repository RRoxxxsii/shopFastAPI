from src.domain.shop.dto.auth import UserDTO
from src.domain.shop.dto.item import ItemDTO
from src.domain.shop.dto.partner import PartnerDTO, UserPartnerDTO
from src.domain.shop.usecases.partner.usecases import (
    CreatePartnerUserDoesNotExists,
    CreatePartnerUserExists, CreateItem,
)
from src.infrastructure.api_client.partners.client import AbstractAPIClient
from src.infrastructure.database.models.item import Item
from src.infrastructure.database.models.partner import Partner
from src.infrastructure.database.uow import AbstractUnitOfWork


class CreatePartnerUserExistsService:
    def __init__(self, api_client: AbstractAPIClient, uow: AbstractUnitOfWork):
        self.api_client: AbstractAPIClient = api_client
        self.uow: AbstractUnitOfWork = uow

    async def _create_partner(self, dto: UserPartnerDTO):
        return await CreatePartnerUserExists(self.uow, self.api_client)(dto)

    async def execute(self, dto: UserPartnerDTO) -> Partner:
        partner = await self._create_partner(dto)
        return partner


class CreatePartnerUserDoesNotExistsService:
    def __init__(self, api_client: AbstractAPIClient, uow: AbstractUnitOfWork):
        self.api_client: AbstractAPIClient = api_client
        self.uow: AbstractUnitOfWork = uow

    async def _create_partner(self, partner_dto: PartnerDTO, user_dto: UserDTO):
        return await CreatePartnerUserDoesNotExists(self.uow, self.api_client)(partner_dto, user_dto)

    async def execute(self, partner_dto: PartnerDTO, user_dto: UserDTO) -> Partner:
        partner = await self._create_partner(partner_dto, user_dto)
        return partner


class CreateItemService:

    def __init__(self, uow: AbstractUnitOfWork):
        self.uow: AbstractUnitOfWork = uow

    async def _create_item(self, dto: ItemDTO) -> Item:
        item = await CreateItem(self.uow)(dto)
        return item

    async def execute(self, dto: ItemDTO) -> Item:
        item = await self._create_item(dto)
        return item
