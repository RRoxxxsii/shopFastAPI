from fastapi import Depends

from src.api.partners.client import Client
from src.models.auth import User
from src.models.partners import Seller
from src.repositories.partners import PartnerRepository
from src.schemas.partners import SellerIn
from src.services.base import BaseService, CreateUser


class PartnerService(BaseService, CreateUser):
    api_client = Client

    def __init__(self, partner_repository: PartnerRepository = Depends(), api_client: Client = Depends()):
        self.repository = partner_repository
        self.api_client = api_client

    async def get_seller_or_none(self, seller_schema) -> [Seller | None]:

        seller = await self.repository.get_seller_or_none(
            tin=seller_schema.tin,
            an=seller_schema.an,
            company_name=seller_schema.company_name,
            mobile=seller_schema.mobile
        )
        return seller

    async def create_seller(self, seller_schema, user: User) -> Seller:
        seller = Seller(
            user=user, bic=seller_schema.bic, tin=seller_schema.tin, trrc=seller_schema.trrc,
            company_name=seller_schema.company_name, company_description=seller_schema.company_description,
            mobile=seller_schema.mobile, an=seller_schema.an, bank_name=seller_schema.bank_name,
            additional=seller_schema.additional
        )
        return await self.repository.create_seller(seller=seller)

    async def validate_data(self, seller_schema) -> bool:

        return await self.api_client.call(
            f'https://htmlweb.ru/api.php?obj=validator&m=kpp&kpp={seller_schema.trrc}',
            f'https://htmlweb.ru/api.php?obj=validator&m=bic&bic={seller_schema.bic}',
            f'https://htmlweb.ru/api.php?obj=validator&m=inn&inn={seller_schema.tin}',
            f'https://htmlweb.ru/api.php?obj=validator&m=phone&phone={seller_schema.mobile}'
        )
