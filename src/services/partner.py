from typing import Type

from src.api.partners.client import AbstractClient
from src.dto.partner import UserPartnerDTO
from src.exceptions.partner import DataNotValid, SellerExists
from src.exceptions.user import UserExists
from src.models.auth import User
from src.models.partners import Seller
from src.repositories.partner import AbstractPartnerRepository
from src.repositories.user import AbstractUserRepository
from src.secure.pwd import PwdAbstract
from src.services.user import CreateUserService


class CreatePartnerMixin:

    def __init__(self, partner_repo: Type[AbstractPartnerRepository], api_client: Type[AbstractClient]):
        self.partner_repo: AbstractPartnerRepository = partner_repo()
        self.api_client: AbstractClient = api_client()

    async def _get_seller_or_none(self, dto) -> Seller | None:
        seller = await self.partner_repo.get_partner_or_none(dto=dto)
        return seller

    async def _validate_data(self, dto) -> bool:
        return await self.api_client.call(
            f'https://htmlweb.ru/api.php?obj=validator&m=kpp&kpp={dto.trrc}',
            f'https://htmlweb.ru/api.php?obj=validator&m=bic&bic={dto.bic}',
            f'https://htmlweb.ru/api.php?obj=validator&m=inn&inn={dto.tin}',
            f'https://htmlweb.ru/api.php?obj=validator&m=phone&phone={dto.mobile}'
        )

    async def _create_seller(self, dto, user_id: int) -> Seller:
        dto = UserPartnerDTO(
            **dto.model_dump(), user_id=user_id
        )
        return await self.partner_repo.create(dto)


class CreatePartnerNotUserExistsService(CreateUserService, CreatePartnerMixin):

    def __init__(
            self,
            partner_repo: Type[AbstractPartnerRepository],
            user_repo: Type[AbstractUserRepository],
            api_client: Type[AbstractClient],
            pwd: Type[PwdAbstract]
    ):
        super().__init__(user_repo, pwd)
        self.partner_repo: AbstractPartnerRepository = partner_repo()
        self.api_client = api_client()

    async def _get_user_or_none(self, email) -> User | None:
        user = await self.user_repo.get_user_by_email(email)
        return user

    async def execute(self, dto) -> Seller | None:
        user = await self._get_user_or_none(dto.email)
        if user:
            raise UserExists('User with this email already exists')
        seller = await self._get_seller_or_none(dto)
        if seller:
            raise SellerExists('Seller with this credentials already exists')
        is_valid = await self._validate_data(dto)
        if not is_valid:
            raise DataNotValid('Data you provided is not valid')
        hashed_password = self._hash_password(dto.password1)
        user = await self._create_user(dto, hashed_password=hashed_password)
        seller = await self._create_seller(dto=dto, user_id=user.id)
        return seller


class CreatePartnerUserExistsService(CreatePartnerMixin):
    def __init__(
            self,
            partner_repo: Type[AbstractPartnerRepository],
            api_client: Type[AbstractClient]
    ):
        super().__init__(partner_repo, api_client)

    async def execute(self, dto, user: User) -> Seller:
        is_valid = await self._validate_data(dto)
        if not is_valid:
            raise DataNotValid('Data you provided is not valid')
        seller = await self._get_seller_or_none(dto)
        if seller:
            raise SellerExists('Seller with this credentials already exists')
        return await self._create_seller(dto, user_id=user.id)
