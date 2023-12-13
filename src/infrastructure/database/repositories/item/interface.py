from abc import ABC, abstractmethod

from src.domain.shop.dto.item import ItemDTO
from src.infrastructure.database.repositories.base import AbstractRepository


class AbstractItemRepository(AbstractRepository, ABC):
    @abstractmethod
    def get_item_or_none(self, item: ItemDTO):
        raise NotImplementedError
