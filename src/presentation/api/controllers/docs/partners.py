from starlette import status

# RESPONSES
upgrade_to_partner = {
    status.HTTP_409_CONFLICT:
    {
        "description": "Unique constraint failed (e.g. tin)",
        "content": {
            "application/json": {
                "example": {'detail': 'User with these already exists'}
            }
        },
    },
    status.HTTP_400_BAD_REQUEST:
    {
        "description": "Validation by special algorithms didn't pass successfully",
        "content": {
            "application/json": {
                "example": {'detail': 'Credentials are not valid'}
            }
        },
    },
    status.HTTP_401_UNAUTHORIZED:
    {
        "description": "Token not provided",
        "content": {
            "application/json": {
                "example": {'detail': 'FORBIDDEN'}
            }

        }
    }
}

register_as_partner = {
    status.HTTP_409_CONFLICT:
    {
        "description": "Unique constraint failed (e.g. tin)",
        "content": {
            "application/json": {
                "example": {'detail': 'User with these already exists'}
            }
        },
    },
    status.HTTP_400_BAD_REQUEST:
    {
        "description": "Validation by special algorithms didn't pass successfully",
        "content": {
            "application/json": {
                "example": {'detail': 'Credentials are not valid'}
            }
        },
    },
}
