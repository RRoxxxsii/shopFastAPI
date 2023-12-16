from fastapi import Depends

from src.domain.shop.services.item import ItemDetailService, ItemListService
from src.domain.shop.services.partner import (
    CreateItemService,
    CreatePartnerUserDoesNotExistsService,
    CreatePartnerUserExistsService,
)
from src.domain.shop.services.user import CreateTokenService, CreateUserService
from src.infrastructure.api_client.partners.interface import AbstractAPIClient
from src.infrastructure.database.uow import AbstractUnitOfWork
from src.presentation.api.di.client import get_aiohttp_client
from src.presentation.api.di.database import get_sqlalchemy_uow


def create_token_service(uow: AbstractUnitOfWork = Depends(get_sqlalchemy_uow)) -> CreateTokenService:
    return CreateTokenService(uow)


def create_user_service(uow: AbstractUnitOfWork = Depends(get_sqlalchemy_uow)) -> CreateUserService:
    return CreateUserService(uow)


def create_item_service(uow: AbstractUnitOfWork = Depends(get_sqlalchemy_uow)) -> CreateItemService:
    return CreateItemService(uow)


def create_partner_user_does_not_exist_service(
    uow: AbstractUnitOfWork = Depends(get_sqlalchemy_uow),
    api_client: AbstractAPIClient = Depends(get_aiohttp_client),
) -> CreatePartnerUserDoesNotExistsService:
    return CreatePartnerUserDoesNotExistsService(api_client, uow)


def create_partner_user_exists_service(
    uow: AbstractUnitOfWork = Depends(get_sqlalchemy_uow),
    api_client: AbstractAPIClient = Depends(get_aiohttp_client),
) -> CreatePartnerUserExistsService:
    return CreatePartnerUserExistsService(api_client, uow)


def get_item_by_id_service(uow: AbstractUnitOfWork = Depends(get_sqlalchemy_uow)) -> ItemDetailService:
    return ItemDetailService(uow)


def get_list_item_service(uow: AbstractUnitOfWork = Depends(get_sqlalchemy_uow)) -> ItemListService:
    return ItemListService(uow)
