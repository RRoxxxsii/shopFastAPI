from pydantic import BaseModel, Field

from src.domain.shop.dto.auth import UserDTO


class PartnerDTO(BaseModel):
    mobile: str
    company_name: str
    company_description: str
    bank_name: str
    tin: str = Field()
    bic: str
    trrc: str
    an: str
    additional: str | None = None


class UserPartnerDTO(PartnerDTO):
    user_id: int


class FullUserPartnerDTO(UserDTO, UserPartnerDTO):
    pass
