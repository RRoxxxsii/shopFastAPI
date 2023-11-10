from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from src.partners import schemas
from src.partners.dependencies import become_partner_service
from src.partners.service import BecomePartnerService
from src.secure import apikey_scheme

router = APIRouter()


@router.post('/register-as-seller/')
def become_partner_no_account():
    """
    Create account for the first times as partner,
    when no account for the same user with same
    credentials in common does not exist
    """
    pass


@router.post('/upgrade-to-seller/', response_model=schemas.SellerOut, status_code=status.HTTP_201_CREATED,
             responses={
                 status.HTTP_409_CONFLICT:
                     {
                         "description": "Unique constraint failed (e.g. tin)",
                         "content": {
                             "application/json": {
                                 "example": {'detail': 'User with these already exists'}
                             }
                         },
                     },
                 }
             )
async def become_partner_exist_account(
        access_token: Annotated[str, Depends(apikey_scheme)],
        service: BecomePartnerService = Depends(become_partner_service)
):

    db_seller = await service.get_seller_exists()
    if db_seller:
        raise HTTPException(
            status.HTTP_409_CONFLICT, 'User with these credentials already exists'
        )

    is_valid = await service.validate_data()
    if not is_valid:
        raise HTTPException(
            status.HTTP_409_CONFLICT, 'Credentials are not valid'
        )
    user = await service.get_user_by_token(access_token)
    seller = await service.create_seller(user)
    return seller
