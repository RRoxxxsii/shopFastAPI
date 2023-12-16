from sqladmin import ModelView

from src.infrastructure.database.models.item import Category, Item


class CategoryAdmin(ModelView, model=Category):
    column_list = [
        Category.id,
        Category.title,
        Category.description,
        Category.data,
    ]


class ItemAdmin(ModelView, model=Item):
    column_list = [
        Item.id,
        Item.title,
        Item.description,
        Item.price,
        Item.partner,
        Item.partner_id,
        Item.category,
        Item.category_id,
        Item.time_created
    ]
