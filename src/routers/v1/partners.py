from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from src.schemas.partners import SellerIn, SellerOut
from src.secure import apikey_scheme
from src.services.partners import PartnerService

router = APIRouter()


@router.post('/upgrade-to-seller/', response_model=SellerOut, status_code=status.HTTP_201_CREATED,
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
        seller_schema: SellerIn,
        access_token: Annotated[str, Depends(apikey_scheme)],
        service: PartnerService = Depends()
):

    db_seller = await service.get_seller_or_none(seller_schema=seller_schema)
    if db_seller:
        raise HTTPException(
            status.HTTP_409_CONFLICT, 'User with these credentials already exists'
        )

    is_valid = await service.validate_data(seller_schema=seller_schema)
    if not is_valid:
        raise HTTPException(
            status.HTTP_409_CONFLICT, 'Credentials are not valid'
        )
    user = await service.get_user_by_token(access_token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='UNAUTHORIZED'
        )

    seller = await service.create_seller(seller_schema, user=user)
    return seller
