from sqlalchemy import select

from src.domain.shop.dto.item import ItemDTO
from src.infrastructure.database.models.item import Item
from src.infrastructure.database.repositories.base import SQLAlchemyRepository
from src.infrastructure.database.repositories.item.interface import (
    AbstractItemRepository,
)


class ItemRepository(AbstractItemRepository, SQLAlchemyRepository):
    model = Item

    async def get_item_or_none(self, dto: ItemDTO):
        stmt = select(Item).where(
            Item.title == dto.title,
        )
        result = await self.session.execute(stmt)
        partner = result.scalar_one_or_none()
        return partner
