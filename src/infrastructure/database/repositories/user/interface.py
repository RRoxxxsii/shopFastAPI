from abc import ABC, abstractmethod

from src.infrastructure.database.repositories.base import AbstractRepository


class AbstractUserRepository(AbstractRepository, ABC):

    @abstractmethod
    def get_user_or_none(self, email: str):
        raise NotImplementedError
