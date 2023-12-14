import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Json


class ItemOut(BaseModel):
    id: int
    title: str
    description: str
    price: Decimal
    data: Json
    category_id: int
    partner_id: int
    time_created: datetime.datetime


class ItemIn(BaseModel):
    title: str
    description: str
    price: Decimal
    data: Json
    category_id: int


class ItemListOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    price: Decimal
    category_id: int
    partner_id: int
