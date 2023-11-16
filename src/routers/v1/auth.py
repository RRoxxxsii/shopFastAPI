from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from src.schemas.auth import LoginUserIn, RegisterUserIn, RegisterUserOut
from src.services.auth import AuthService

router = APIRouter()


@router.post('/create-token/', status_code=status.HTTP_201_CREATED)
async def create_token(user_schema: LoginUserIn, service: AuthService = Depends()):

    db_user = await service.get_user_or_none(email=user_schema.email)

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User with provided credentials not found'
        )
    if not service.check_password(password=user_schema.password, hashed_password=db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Incorrect password'
        )

    token = await service.create_token(db_user.id)
    return token


@router.post('/sign-up/', response_model=RegisterUserOut, status_code=status.HTTP_201_CREATED,
             responses={
                 status.HTTP_409_CONFLICT:
                     {
                         "description": "Unique constraint failed (e.g. password)",
                         "content": {
                             "application/json": {
                                 "example": {'detail': 'User with <field> <value> already exists'}
                             }
                         },
                     },
                 }
             )
async def register(user_schema: RegisterUserIn, service: AuthService = Depends()):

    hashed_password = service.hash_password(user_schema.password1)
    db_user = await service.get_user_or_none(user_schema.email)
    if db_user:
        raise HTTPException(
            status.HTTP_409_CONFLICT, f'User with email {db_user.email} already exists'
        )

    user = await service.create_user(user_schema=user_schema, hashed_password=hashed_password)
    return user
