from abc import ABC

from src.infrastructure.database.repositories.base import AbstractRepository


class AbstractTokenRepository(AbstractRepository, ABC):
    pass
