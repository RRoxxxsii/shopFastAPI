import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, Json

from src.presentation.api.controllers.v1.responses.auth import RegisterUserOut


class PartnerOut(BaseModel):
    id: int
    user_id: int
    mobile: str
    company_name: str
    company_description: str
    bank_name: str
    tin: str = Field()
    bic: str
    trrc: str
    an: str
    additional: str | None = None


class UserPartnerOut(PartnerOut, RegisterUserOut):
    pass


class ItemOut(BaseModel):
    id: int
    title: str
    description: str
    price: Decimal
    data: Json
    # images: list[ImageDTO]

    category_id: int
    partner_id: int
    time_created: datetime.datetime

