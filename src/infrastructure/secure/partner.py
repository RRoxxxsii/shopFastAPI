from fastapi import Depends, HTTPException
from starlette import status

from src.infrastructure.database.models.auth import User
from src.infrastructure.database.models.partner import Partner
from src.infrastructure.secure.user import get_current_user


def get_current_partner(user: User = Depends(get_current_user)) -> Partner:
    if user.is_partner:
        partner = user.partner
        return partner
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="NOT PARTNER")


def get_current_partner_approved(partner: Partner = Depends(get_current_partner)) -> Partner:
    if partner.is_approved:
        return partner
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="NOT APPROVED")
