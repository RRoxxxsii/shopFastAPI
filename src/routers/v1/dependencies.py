from fastapi import Depends

from src.api.partners.client import AbstractAPIClient, Client
from src.database import async_session_maker
from src.database.uow import AbstractUnitOfWork, UnitOfWork
from src.services.partner import (CreatePartnerUserDoesNotExistsService,
                                  CreatePartnerUserExistsService)
from src.services.user import CreateTokenService, CreateUserService


def get_sqlalchemy_uow():
    return UnitOfWork(async_session_maker)


def create_token_service(uow: AbstractUnitOfWork = Depends(get_sqlalchemy_uow)):
    return CreateTokenService(uow)


def create_user_service(uow: AbstractUnitOfWork = Depends(get_sqlalchemy_uow)):
    return CreateUserService(uow)


def create_seller_user_does_not_exist_service(
        uow: AbstractUnitOfWork = Depends(get_sqlalchemy_uow),
        api_client: AbstractAPIClient = Depends(Client)
):
    return CreatePartnerUserDoesNotExistsService(api_client, uow)


def create_seller_user_exists_service(
        uow: AbstractUnitOfWork = Depends(get_sqlalchemy_uow),
        api_client: AbstractAPIClient = Depends(Client)
):
    return CreatePartnerUserExistsService(api_client, uow)


# UOWDep = Annotated[AbstractUnitOfWork, Depends(get_sqlalchemy_uow)]
#
# APIClientDep = Annotated[AbstractAPIClient, Depends(Client)]
