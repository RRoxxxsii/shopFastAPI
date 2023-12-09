from typing import Optional

from pydantic import BaseModel, Field

from src.routers.v1.responses.auth import RegisterUserOut


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
    additional: Optional[str] = None


class UserPartnerOut(PartnerOut, RegisterUserOut):
    pass
