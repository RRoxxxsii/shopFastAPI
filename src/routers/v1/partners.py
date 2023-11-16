from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from src.routers.docs.partners import register_as_partner, upgrade_to_seller
from src.routers.responses import BaseResponse
from src.schemas.partners import SellerIn, SellerOut, UserSellerIn
from src.secure import apikey_scheme
from src.services.partners import PartnerService

router = APIRouter()


@router.post('/upgrade-to-seller/', response_model=SellerOut, status_code=status.HTTP_201_CREATED,
             responses=upgrade_to_seller)
async def become_partner_exist_account(
        seller_schema: SellerIn,
        access_token: Annotated[str, Depends(apikey_scheme)],
        service: PartnerService = Depends()
):

    db_seller = await service.get_seller_or_none(seller_schema=seller_schema)
    if db_seller:
        BaseResponse.raise_409()

    is_valid = await service.validate_data(seller_schema=seller_schema)
    if not is_valid:
        BaseResponse.raise_400()

    user = await service.get_user_by_token(access_token)
    if not user:
        BaseResponse.raise_401()
    seller = await service.create_seller(seller_schema, user=user)
    return seller


@router.post('/register-as-partner/', response_model=SellerOut, status_code=status.HTTP_201_CREATED,
             responses=register_as_partner)
async def register_as_partner(
        seller_schema: UserSellerIn,
        service: PartnerService = Depends()
):
    db_user = await service.get_user_or_none(email=seller_schema.email)
    if db_user:
        BaseResponse.raise_409()

    db_seller = await service.get_seller_or_none(seller_schema)
    if db_seller:
        BaseResponse.raise_409()

    is_valid = await service.validate_data(seller_schema=seller_schema)
    if not is_valid:
        BaseResponse.raise_400()

    hashed_password = service.hash_password(seller_schema.password1)

    user = await service.create_user(user_schema=seller_schema, hashed_password=hashed_password)
    seller = await service.create_seller(user=user, seller_schema=seller_schema)
    return seller
