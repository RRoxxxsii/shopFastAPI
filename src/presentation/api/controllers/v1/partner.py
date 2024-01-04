import json

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from src.domain.shop.dto.auth import UserDTO
from src.domain.shop.dto.item import ItemDTO
from src.domain.shop.dto.partner import PartnerDTO, UserPartnerDTO
from src.domain.shop.exceptions.category import (
    CategoryDataDoesNotMatch,
    CategoryDoesNotExist,
)
from src.domain.shop.exceptions.item import ItemExists
from src.domain.shop.exceptions.partner import DataNotValid, PartnerExists
from src.domain.shop.exceptions.user import UserExists
from src.domain.shop.services.partner import (
    CreateItemService,
    CreatePartnerUserDoesNotExistsService,
    CreatePartnerUserExistsService,
)
from src.infrastructure.database.models.auth import User
from src.infrastructure.database.models.partner import Partner
from src.infrastructure.secure.partner import get_current_partner_approved
from src.infrastructure.secure.user import get_current_user
from src.presentation.api.controllers.docs.partner import (
    create_item,
    register_as_partner,
    upgrade_to_partner,
)
from src.presentation.api.controllers.v1.requests.partners import (
    PartnerIn,
    UserPartnerIn,
)
from src.presentation.api.controllers.v1.responses.item import ItemIn, ItemOut
from src.presentation.api.controllers.v1.responses.partners import PartnerOut
from src.presentation.api.di.services import (
    create_item_service,
    create_partner_user_does_not_exist_service,
    create_partner_user_exists_service,
)

router = APIRouter()


@router.post(
    "/register-as-partner/",
    response_model=PartnerOut,
    status_code=status.HTTP_201_CREATED,
    responses=register_as_partner,
)
async def become_partner_no_account(
    partner_schema: UserPartnerIn,
    service: CreatePartnerUserDoesNotExistsService = Depends(create_partner_user_does_not_exist_service),
):
    partner_dto = PartnerDTO(
        **partner_schema.model_dump(exclude={"password1", "password2", "name", "surname", "email"})
    )
    user_dto = UserDTO(**partner_schema.model_dump(include={"password1", "name", "surname", "email"}))

    try:
        partner = await service.execute(partner_dto, user_dto)
    except UserExists:
        raise HTTPException(status.HTTP_409_CONFLICT, "User with these credentials already exists")
    except PartnerExists:
        raise HTTPException(status.HTTP_409_CONFLICT, "Partner with these credentials already exists")
    except DataNotValid:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Credentials are not valid")
    else:
        return partner


@router.post(
    "/upgrade-to-partner/",
    response_model=PartnerOut,
    status_code=status.HTTP_201_CREATED,
    responses=upgrade_to_partner,
)
async def become_partner_exist_account(
    partner_schema: PartnerIn,
    service: CreatePartnerUserExistsService = Depends(create_partner_user_exists_service),
    user: User = Depends(get_current_user),
):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="UNAUTHORIZED")

    try:
        partner = await service.execute(UserPartnerDTO(**partner_schema.model_dump(), user_id=user.id))
    except PartnerExists:
        raise HTTPException(status.HTTP_409_CONFLICT, "Partner with these credentials already exists")
    except DataNotValid:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Credentials are not valid")
    else:
        return partner


@router.post("/create-item/", response_model=ItemOut, status_code=status.HTTP_201_CREATED, responses=create_item)
async def partner_create_item(
    item_schema: ItemIn,
    service: CreateItemService = Depends(create_item_service),
    partner: Partner = Depends(get_current_partner_approved),
):
    item_dto = ItemDTO(
        partner_id=partner.id, data=json.dumps(item_schema.data), **item_schema.model_dump(exclude={"data"})
    )
    try:
        item = await service.execute(item_dto)
    except ItemExists:
        raise HTTPException(status.HTTP_409_CONFLICT, "Item with these credentials already exists")
    except CategoryDoesNotExist:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Category does not exist")
    except CategoryDataDoesNotMatch:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Category data does not match required format")
    else:
        item.data = json.dumps(item.data)
        return item
