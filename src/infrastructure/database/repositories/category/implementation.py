from src.infrastructure.database.models.item import Category
from src.infrastructure.database.repositories.base import SQLAlchemyRepository
from src.infrastructure.database.repositories.category.interface import (
    AbstractCategoryRepository
)


class CategoryRepository(AbstractCategoryRepository, SQLAlchemyRepository):
    model = Category
