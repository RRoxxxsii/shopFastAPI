from pydantic import BaseModel, Field

from src.presentation.api.controllers.v1.requests.auth import RegisterUserIn


class PartnerIn(BaseModel):
    mobile: str
    company_name: str
    company_description: str
    bank_name: str
    tin: str = Field()
    bic: str
    trrc: str
    an: str
    additional: str | None = None


class UserPartnerIn(PartnerIn, RegisterUserIn):
    pass
