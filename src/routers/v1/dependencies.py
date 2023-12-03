from src.api.partners.client import Client
from src.repositories.partner import PartnerRepository
from src.repositories.token import TokenRepository
from src.services.partner import CreatePartnerNotUserExistsService, CreatePartnerUserExistsService
from src.services.user import CreateUserService, CreateTokenService
from src.repositories.user import UserRepository
from src.secure.pwd import PwdImpl


def create_user_service():
    return CreateUserService(UserRepository, PwdImpl)


def create_token_service():
    return CreateTokenService(UserRepository, TokenRepository, PwdImpl)


def create_partner_user_not_exists():
    return CreatePartnerNotUserExistsService(PartnerRepository, UserRepository, Client, PwdImpl)


def create_partner_user_exists():
    return CreatePartnerUserExistsService(PartnerRepository, Client)
