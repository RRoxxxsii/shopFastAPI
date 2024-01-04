from starlette import status

# RESPONSES
upgrade_to_partner = {
    status.HTTP_409_CONFLICT: {
        "description": "Unique constraint failed (e.g. tin)",
        "content": {"application/json": {"example": {"detail": "User with these already exists"}}},
    },
    status.HTTP_400_BAD_REQUEST: {
        "description": "Validation by special algorithms didn't pass successfully",
        "content": {"application/json": {"example": {"detail": "Credentials are not valid"}}},
    },
    status.HTTP_401_UNAUTHORIZED: {
        "description": "Token not provided",
        "content": {"application/json": {"example": {"detail": "FORBIDDEN"}}},
    },
}

register_as_partner = {
    status.HTTP_409_CONFLICT: {
        "description": "Unique constraint failed (e.g. tin)",
        "content": {"application/json": {"example": {"detail": "User with these already exists"}}},
    },
    status.HTTP_400_BAD_REQUEST: {
        "description": "Validation by special algorithms didn't pass successfully",
        "content": {"application/json": {"example": {"detail": "Credentials are not valid"}}},
    },
}

create_item = {
    status.HTTP_409_CONFLICT: {
        "description": "Item with provided by partner credentials on unique constraint already exists",
        "content": {"application/json": {"example": {"detail": "Item with these credentials already exists"}}}
    },
    status.HTTP_400_BAD_REQUEST: {
        "description": "Category with provided category ID does not exists or category data provided in data item"
                       "does not match category data format for this category ID",
        "content": {"application/json": {"example": {"detail": "Category does not exist"}}},
    },
}
