from starlette import status

# RESPONSES
sign_up = {
    status.HTTP_409_CONFLICT: {
        "description": "Unique constraint failed (e.g. password)",
        "content": {"application/json": {"example": {"detail": "User with <field> <value> already exists"}}},
    },
}
