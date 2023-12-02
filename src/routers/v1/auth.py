from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from src.routers.docs.auth import sign_up
from src.routers.v1.dependencies import create_user_service
from src.schemas.auth import RegisterUserIn, RegisterUserOut
from src.services.user import CreateUserService

router = APIRouter()


# @router.post('/create-token/', status_code=status.HTTP_201_CREATED)
# async def create_token(user_schema: LoginUserIn, service: AuthService = Depends()):
#
#     db_user = await service.get_user_or_none(email=user_schema.email)
#     if not db_user:
#         BaseResponse.raise_404('User with provided credentials not found')
#
#     if not service.check_password(password=user_schema.password, hashed_password=db_user.hashed_password):
#         BaseResponse.raise_400('Incorrect password')
#
#     token = await service.create_token(db_user.id)
#     return token
#

@router.post('/sign-up/', response_model=RegisterUserOut, status_code=status.HTTP_201_CREATED,
             responses=sign_up)
async def register(user_schema: RegisterUserIn, service: CreateUserService = Depends(create_user_service)):

    user = await service.execute(dto=user_schema)
    return user
