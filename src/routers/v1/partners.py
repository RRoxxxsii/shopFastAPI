from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from src.exceptions.partner import DataNotValid, SellerExists
from src.exceptions.user import UserExists
from src.models.auth import User
from src.routers.docs.partners import register_as_partner, upgrade_to_seller
from src.routers.v1.dependencies import (create_partner_user_exists,
                                         create_partner_user_not_exists)
from src.routers.v1.requests.partners import SellerIn, UserSellerIn
from src.routers.v1.responses.partners import SellerOut
from src.secure.user import get_current_user
from src.services.partner import (CreatePartnerNotUserExistsService,
                                  CreatePartnerUserExistsService)

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
        raise HTTPException(status.HTTP_409_CONFLICT, 'User with these credentials already exists')
    except SellerExists:
        raise HTTPException(status.HTTP_409_CONFLICT, 'Seller with these credentials already exists')
    except DataNotValid:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Credentials are not valid')
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
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='UNAUTHORIZED')

    try:
        seller = await service.execute(dto=seller_schema, user=user)
    except SellerExists:
        raise HTTPException(status.HTTP_409_CONFLICT, 'Seller with these credentials already exists')
    except DataNotValid:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Credentials are not valid')
    else:
        return seller
