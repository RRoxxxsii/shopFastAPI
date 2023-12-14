from sqlalchemy import select

from src.domain.shop.dto.item import ItemDTO
from src.infrastructure.database.models.item import Item
from src.infrastructure.database.repositories.base import SQLAlchemyRepository
from src.infrastructure.database.repositories.item.interface import (
    AbstractItemRepository,
)


class ItemRepository(AbstractItemRepository, SQLAlchemyRepository):
    model = Item

    async def get_item_or_none(self, dto: ItemDTO) -> Item:
        stmt = select(self.model).where(
            self.model.title == dto.title,
        )
        result = await self.session.execute(stmt)
        item = result.scalar_one_or_none()
        return item
