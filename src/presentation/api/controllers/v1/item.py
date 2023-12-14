import json

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from src.domain.shop.dto.item import ItemIdDTO
from src.domain.shop.exceptions.item import ItemDoesNotExists
from src.domain.shop.services.item import ItemDetailService, ItemListService
from src.presentation.api.controllers.v1.responses.item import ItemListOut, ItemOut
from src.presentation.api.di.services import (
    get_item_by_id_service,
    get_list_item_service,
)

router = APIRouter()


@router.get("/get-item/", response_model=ItemOut)
async def get_item_by_id(item_id: int, get_item_service: ItemDetailService = Depends(get_item_by_id_service)):
    dto = ItemIdDTO(item_id=item_id)
    try:
        item = await get_item_service.execute(dto)
    except ItemDoesNotExists:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Item with this ID does not exist")
    else:
        item.data = json.dumps(item.data)
        return item


@router.get("/get-all-items/", response_model=list[ItemListOut])
async def get_list_items(get_item_service: ItemListService = Depends(get_list_item_service)):
    items = await get_item_service.execute()
    return items
