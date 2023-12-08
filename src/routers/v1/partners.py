from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from src.dto.auth import CreateUserDTO
from src.dto.partner import PartnerDTO, UserPartnerDTO
from src.exceptions.partner import DataNotValid, SellerExists
from src.exceptions.user import UserExists
from src.models.auth import User
from src.routers.docs.partners import register_as_partner, upgrade_to_seller
from src.routers.v1.dependencies import APIClientDep, UOWDep
from src.routers.v1.requests.partners import SellerIn, UserSellerIn
from src.routers.v1.responses.partners import SellerOut
from src.secure.user import get_current_user
from src.services.partner import (CreatePartnerUserDoesNotExistsService,
                                  CreatePartnerUserExistsService)

router = APIRouter()


@router.post('/register-as-partner/', response_model=SellerOut, status_code=status.HTTP_201_CREATED,
             responses=register_as_partner)
async def register_as_partner(
        seller_schema: UserSellerIn,
        api_client: APIClientDep,
        uow: UOWDep,
):
    service = CreatePartnerUserDoesNotExistsService(api_client, uow)
    partner_dto = PartnerDTO(
        **seller_schema.model_dump(exclude={'password1', 'password2', 'name', 'surname', 'email'}
                                   ))
    user_dto = CreateUserDTO(**seller_schema.model_dump(include={'password1', 'name', 'surname', 'email'}))

    try:
        seller = await service.execute(partner_dto, user_dto)
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
        api_client: APIClientDep,
        uow: UOWDep,
        user: User = Depends(get_current_user),

):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='UNAUTHORIZED')

    service = CreatePartnerUserExistsService(uow=uow, api_client=api_client)
    try:
        seller = await service.execute(UserPartnerDTO(**seller_schema.model_dump(), user_id=user.id))
    except SellerExists:
        raise HTTPException(status.HTTP_409_CONFLICT, 'Seller with these credentials already exists')
    except DataNotValid:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Credentials are not valid')
    else:
        return seller
