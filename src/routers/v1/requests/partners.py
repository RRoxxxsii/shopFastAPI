from typing import Optional

from pydantic import BaseModel, Field

from src.routers.v1.requests.auth import RegisterUserIn


class PartnerIn(BaseModel):
    mobile: str
    company_name: str
    company_description: str
    bank_name: str
    tin: str = Field()
    bic: str
    trrc: str
    an: str
    additional: Optional[str] = None


class UserPartnerIn(PartnerIn, RegisterUserIn):
    pass
