# from typing import Annotated
#
# from fastapi import APIRouter, Depends
# from starlette import status
#
# from src.routers.docs.partners import register_as_partner, upgrade_to_seller
# from src.routers.responses import BaseResponse
# from src.schemas.partners import SellerIn, SellerOut, UserSellerIn
# from src.secure import apikey_scheme
# from src.services.partners import PartnerService
#
# router = APIRouter()
#
#
#
#
from fastapi import Depends, APIRouter
from starlette import status

from src.exceptions.partner import SellerExists, DataNotValid
from src.exceptions.user import UserExists
from src.models.auth import User
from src.routers.docs.partners import register_as_partner, upgrade_to_seller
from src.routers.responses import BaseResponse
from src.routers.v1.dependencies import create_partner_user_not_exists, create_partner_user_exists
from src.routers.v1.responses.partners import SellerOut
from src.routers.v1.requests.partners import UserSellerIn, SellerIn
from src.secure.pwd import get_current_user
from src.services.partner import CreatePartnerNotUserExistsService, CreatePartnerUserExistsService

router = APIRouter()


@router.post('/register-as-partner/', response_model=SellerOut, status_code=status.HTTP_201_CREATED,
             responses=register_as_partner)
async def register_as_partner(
        seller_schema: UserSellerIn,
        service: CreatePartnerNotUserExistsService = Depends(create_partner_user_not_exists)
):
    try:
        seller = await service.execute(dto=seller_schema)
    except UserExists:
        BaseResponse.raise_409()
    except SellerExists:
        BaseResponse.raise_409('Seller with this credentials already exists')
    except DataNotValid:
        BaseResponse.raise_400()
    else:
        return seller


@router.post('/upgrade-to-seller/', response_model=SellerOut, status_code=status.HTTP_201_CREATED,
             responses=upgrade_to_seller)
async def become_partner_exist_account(
        seller_schema: SellerIn,
        user: User = Depends(get_current_user),
        service: CreatePartnerUserExistsService = Depends(create_partner_user_exists)
):
    if not user:
        BaseResponse.raise_401()

    try:
        seller = await service.execute(dto=seller_schema, user=user)
    except SellerExists:
        BaseResponse.raise_409('Seller with this credentials already exists')
    except DataNotValid:
        BaseResponse.raise_400()
    else:
        return seller

