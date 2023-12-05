from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.partners.client import AbstractAPIClient, Client
from src.database import async_session_maker, get_async_session
from src.database.uow import AbstractUnitOfWork, UnitOfWork
from src.repositories.partner import PartnerRepository
from src.repositories.token import TokenRepository
from src.repositories.user import UserRepository
from src.services.partner import CreatePartnerUserExistsService
from src.services.user import CreateTokenService, CreateUserService

# def create_user_service():
#     return CreateUserService(UserRepository, PwdImpl)


# def create_token_service():
#     return CreateTokenService(UserRepository, TokenRepository, PwdImpl)


# def create_partner_user_not_exists():
#     return CreatePartnerNotUserExistsService(PartnerRepository, UserRepository, Client, PwdImpl)


# def create_partner_user_exists():
#     return CreatePartnerUserExistsService(PartnerRepository, Client)


# def get_user_services(session: AsyncSession = Depends(async_session_maker)) -> CreatePartnerUserExistsService:
#     return CreatePartnerUserExistsService(Client, UnitOfWork(session))


UOWDep = Annotated[AbstractUnitOfWork, Depends(UnitOfWork)]

APIClientDep = Annotated[AbstractAPIClient, Depends(Client)]
