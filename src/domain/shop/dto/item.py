from decimal import Decimal

from pydantic import BaseModel, Json


class ImageDTO(BaseModel):
    image_url: str


class ItemDTO(BaseModel):
    title: str
    description: str
    price: Decimal
    data: Json
    # images: list[ImageDTO]

    category_id: int
    partner_id: int
