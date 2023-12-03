from fastapi import APIRouter, Depends
from starlette import status

from src.exceptions.user import PasswordIsNotCorrect, UserExists, UserNotFound
from src.routers.docs.auth import sign_up
from src.routers.responses import BaseResponse
from src.routers.v1.dependencies import (create_token_service,
                                         create_user_service)
from src.routers.v1.requests.auth import LoginUserIn, RegisterUserIn
from src.routers.v1.responses.auth import RegisterUserOut
from src.services.user import CreateTokenService, CreateUserService

router = APIRouter()


@router.post('/create-token/', status_code=status.HTTP_201_CREATED)
async def create_token(user_schema: LoginUserIn, service: CreateTokenService = Depends(create_token_service)):

    try:
        token = await service.execute(dto=user_schema)
    except UserNotFound:
        raise BaseResponse.raise_404()
    except PasswordIsNotCorrect:
        raise BaseResponse.raise_400()
    else:
        return token


@router.post('/sign-up/', response_model=RegisterUserOut, status_code=status.HTTP_201_CREATED,
             responses=sign_up)
async def register(user_schema: RegisterUserIn, service: CreateUserService = Depends(create_user_service)):
    try:
        user = await service.execute(dto=user_schema)
    except UserExists:
        raise BaseResponse.raise_409()
    else:
        return user
