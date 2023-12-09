from src.infrastructure.database.uow import AbstractUnitOfWork
from src.domain.common.usecases.base import BaseUseCase


class BaseExtendedUseCase(BaseUseCase):
    def __init__(self, uow: AbstractUnitOfWork) -> None:
        super().__init__(uow)


