from src.domain.shop.dto.item import ItemIdDTO
from src.domain.shop.usecases.item.usecases import GetItemById
from src.infrastructure.database.models.item import Item
from src.infrastructure.database.uow import AbstractUnitOfWork


class ItemService:
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow: AbstractUnitOfWork = uow

    async def _get_item_by_id(self, dto: ItemIdDTO) -> Item:
        return await GetItemById(self.uow)(dto)

    async def execute(self, dto: ItemIdDTO) -> Item:
        item = await self._get_item_by_id(dto)
        return item
