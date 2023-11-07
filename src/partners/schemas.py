from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

from src.schemas import BaseUser


class SellerIn(BaseModel):
    mobile: str
    company_name: str
    company_description: str
    bank_name: str
    tin: str = Field()
    bic: str
    trrc: str
    an: str
    additional: Optional[str] = None


class SellerOut(SellerIn):
    id: int
    user_id: int
