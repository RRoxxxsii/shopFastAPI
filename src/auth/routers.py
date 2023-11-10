from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from src.auth import schemas
from src.auth.dependencies import get_auth_service
from src.auth.service import AuthService
from src.secure import pwd_context

router = APIRouter()


@router.post('/create-token/')
async def create_token(user: schemas.LoginUserIn, service: AuthService = Depends(get_auth_service)):

    db_user = await service.get_user_exists(email=user.email)

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User with provided credentials not found'
        )

    if not pwd_context.verify(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Incorrect password'
        )

    token = await service.create_token(db_user)
    return token


@router.post('/sign-up/', response_model=schemas.RegisterUserOut, status_code=status.HTTP_201_CREATED,
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
async def register(user: schemas.RegisterUserIn, service: AuthService = Depends(get_auth_service)):
    hashed_password = pwd_context.hash(user.password1)

    db_user = await service.get_user_exists(user.email)

    if db_user:
        raise HTTPException(
            status.HTTP_409_CONFLICT, f'User with email {db_user.email} already exists'
        )

    user = await service.create_user(user, hashed_password)
    return user
