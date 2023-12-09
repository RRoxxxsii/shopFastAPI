from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from src.domain.shop.dto.auth import AuthDTO, CreateUserDTO
from src.domain.shop.exceptions.user import (
    PasswordIsNotCorrect,
    UserExists,
    UserNotFound,
)
from src.domain.shop.services.user import CreateTokenService, CreateUserService
from src.presentation.api.controllers.docs.auth import sign_up
from src.presentation.api.controllers.v1.requests.auth import (
    LoginUserIn,
    RegisterUserIn,
)
from src.presentation.api.controllers.v1.responses.auth import RegisterUserOut
from src.presentation.api.di.services import create_token_service, create_user_service

router = APIRouter()


@router.post("/create-token/", status_code=status.HTTP_201_CREATED)
async def create_token(
    user_schema: LoginUserIn,
    service: CreateTokenService = Depends(create_token_service),
):
    user_dto = AuthDTO(**user_schema.model_dump())

    try:
        token = await service.execute(user_dto)
    except UserNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    except PasswordIsNotCorrect:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Credentials are not valid")
    else:
        return token


@router.post(
    "/sign-up/",
    response_model=RegisterUserOut,
    status_code=status.HTTP_201_CREATED,
    responses=sign_up,
)
async def register(
    user_schema: RegisterUserIn,
    service: CreateUserService = Depends(create_user_service),
):
    user_dto = CreateUserDTO(**user_schema.model_dump(exclude={"password2"}))
    try:
        user = await service.execute(user_dto)
    except UserExists:
        raise HTTPException(status.HTTP_409_CONFLICT, "User with these credentials already exists")
    else:
        return user
