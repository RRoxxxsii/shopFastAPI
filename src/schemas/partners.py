from typing import Optional

from pydantic import BaseModel, Field

from src.schemas.auth import RegisterUserIn, RegisterUserOut


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


class UserSellerOut(SellerOut, RegisterUserOut):
    pass


class UserSellerIn(SellerIn, RegisterUserIn):
    pass
