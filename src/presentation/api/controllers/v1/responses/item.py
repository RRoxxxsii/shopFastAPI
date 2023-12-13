import datetime
from decimal import Decimal

from pydantic import BaseModel, Json


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
