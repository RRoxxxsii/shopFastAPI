from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from src.domain.shop.dto.auth import CreateUserDTO
from src.domain.shop.dto.partner import PartnerDTO, UserPartnerDTO
from src.domain.shop.exceptions.partner import DataNotValid, PartnerExists
from src.domain.shop.exceptions.user import UserExists
from src.infrastructure.database.models.auth import User
from src.presentation.api.controllers.docs.partners import register_as_partner, upgrade_to_partner
from src.presentation.api.di.services import create_partner_user_does_not_exist_service, \
    create_partner_user_exists_service
from src.presentation.api.controllers.v1.requests.partners import PartnerIn, UserPartnerIn
from src.presentation.api.controllers.v1.responses.partners import PartnerOut
from src.infrastructure.secure.user import get_current_user
from src.domain.shop.services.partner import (CreatePartnerUserDoesNotExistsService,
                                              CreatePartnerUserExistsService)

router = APIRouter()


@router.post('/register-as-partner/', response_model=PartnerOut, status_code=status.HTTP_201_CREATED,
             responses=register_as_partner)
async def register_as_partner(
        partner_schema: UserPartnerIn,
        service: CreatePartnerUserDoesNotExistsService = Depends(create_partner_user_does_not_exist_service)
):

    partner_dto = PartnerDTO(
        **partner_schema.model_dump(
            exclude={'password1', 'password2', 'name', 'surname', 'email'}
                                   ))
    user_dto = CreateUserDTO(**partner_schema.model_dump(include={'password1', 'name', 'surname', 'email'}))

    try:
        partner = await service.execute(partner_dto, user_dto)
    except UserExists:
        raise HTTPException(status.HTTP_409_CONFLICT, 'User with these credentials already exists')
    except PartnerExists:
        raise HTTPException(status.HTTP_409_CONFLICT, 'Partner with these credentials already exists')
    except DataNotValid:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Credentials are not valid')
    else:
        return partner


@router.post('/upgrade-to-partner/', response_model=PartnerOut, status_code=status.HTTP_201_CREATED,
             responses=upgrade_to_partner)
async def become_partner_exist_account(
        partner_schema: PartnerIn,
        service: CreatePartnerUserExistsService = Depends(create_partner_user_exists_service),
        user: User = Depends(get_current_user),

):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='UNAUTHORIZED')

    try:
        partner = await service.execute(UserPartnerDTO(**partner_schema.model_dump(), user_id=user.id))
    except PartnerExists:
        raise HTTPException(status.HTTP_409_CONFLICT, 'Partner with these credentials already exists')
    except DataNotValid:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Credentials are not valid')
    else:
        return partner
