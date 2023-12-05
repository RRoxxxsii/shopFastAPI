from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from src.exceptions.user import PasswordIsNotCorrect, UserExists, UserNotFound
from src.routers.docs.auth import sign_up
from src.routers.v1.requests.auth import LoginUserIn, RegisterUserIn
from src.routers.v1.responses.auth import RegisterUserOut
from src.services.user import CreateTokenService, CreateUserService

router = APIRouter()

create_token_service = lambda x: x
create_user_service = lambda x: x

@router.post('/create-token/', status_code=status.HTTP_201_CREATED)
async def create_token(user_schema: LoginUserIn, service: CreateTokenService = Depends(create_token_service)):

    try:
        token = await service.execute(dto=user_schema)
    except UserNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not Found')
    except PasswordIsNotCorrect:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Credentials are not valid')
    else:
        return token


@router.post('/sign-up/', response_model=RegisterUserOut, status_code=status.HTTP_201_CREATED,
             responses=sign_up)
async def register(user_schema: RegisterUserIn, service: CreateUserService = Depends(create_user_service)):
    try:
        user = await service.execute(dto=user_schema)
    except UserExists:
        raise HTTPException(status.HTTP_409_CONFLICT, 'User with these credentials already exists')
    else:
        return user
