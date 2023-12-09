from fastapi import Depends

from src.domain.shop.services.partner import (
    CreatePartnerUserDoesNotExistsService,
    CreatePartnerUserExistsService,
)
from src.domain.shop.services.user import CreateTokenService, CreateUserService
from src.infrastructure.api_client.partners.client import AbstractAPIClient, Client
from src.infrastructure.database.uow import AbstractUnitOfWork
from src.presentation.api.di.database import get_sqlalchemy_uow


def create_token_service(uow: AbstractUnitOfWork = Depends(get_sqlalchemy_uow)):
    return CreateTokenService(uow)


def create_user_service(uow: AbstractUnitOfWork = Depends(get_sqlalchemy_uow)):
    return CreateUserService(uow)


def create_partner_user_does_not_exist_service(
    uow: AbstractUnitOfWork = Depends(get_sqlalchemy_uow),
    api_client: AbstractAPIClient = Depends(Client),
):
    return CreatePartnerUserDoesNotExistsService(api_client, uow)


def create_partner_user_exists_service(
    uow: AbstractUnitOfWork = Depends(get_sqlalchemy_uow),
    api_client: AbstractAPIClient = Depends(Client),
):
    return CreatePartnerUserExistsService(api_client, uow)
