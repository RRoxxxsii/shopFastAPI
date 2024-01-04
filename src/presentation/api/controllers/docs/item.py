from starlette import status

get_item = {
    status.HTTP_404_NOT_FOUND: {
        "description": "Item with this ID does not exist",
        "content": {"application/json": {"example": {"detail": "Item with this ID does not exist"}}},
    },
}
