from src.domain.shop.dto.item import ItemIdDTO
from src.domain.shop.exceptions.item import ItemDoesNotExists
from src.domain.shop.usecases.item.base import ItemUseCase
from src.infrastructure.database.models.item import Item


class GetItemById(ItemUseCase):
    async def __call__(self, dto: ItemIdDTO) -> Item:
        async with self.uow:
            item = await self.uow.item_repo.get_by_id(pk=dto.item_id)
            if not item:
                raise ItemDoesNotExists("Item with this id does not exist")
            await self.uow.commit()
            return item
