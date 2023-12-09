from src.domain.shop.usecases.base import BaseExtendedUseCase
from src.infrastructure.api_client.partners.client import AbstractAPIClient
from src.infrastructure.database.uow import AbstractUnitOfWork


class PartnerUseCase(BaseExtendedUseCase):

    def __init__(self, uow: AbstractUnitOfWork, api_client: AbstractAPIClient):
        super().__init__(uow)
        self.api_client: AbstractAPIClient = api_client
