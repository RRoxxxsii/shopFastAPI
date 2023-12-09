from pydantic import BaseModel, Field

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
