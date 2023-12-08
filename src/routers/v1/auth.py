from fastapi import APIRouter, HTTPException
from starlette import status

from src.dto.auth import AuthDTO, CreateUserDTO
from src.exceptions.user import PasswordIsNotCorrect, UserExists, UserNotFound
from src.routers.docs.auth import sign_up
from src.routers.v1.dependencies import UOWDep
from src.routers.v1.requests.auth import LoginUserIn, RegisterUserIn
from src.routers.v1.responses.auth import RegisterUserOut
from src.services.user import CreateTokenService, CreateUserService

router = APIRouter()


@router.post('/create-token/', status_code=status.HTTP_201_CREATED)
async def create_token(user_schema: LoginUserIn, uow: UOWDep):

    service = CreateTokenService(uow)

    user_dto = AuthDTO(**user_schema.model_dump())

    try:
        token = await service.execute(user_dto)
    except UserNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not Found')
    except PasswordIsNotCorrect:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Credentials are not valid')
    else:
        return token


@router.post('/sign-up/', response_model=RegisterUserOut, status_code=status.HTTP_201_CREATED,
             responses=sign_up)
async def register(user_schema: RegisterUserIn, uow: UOWDep):
    service = CreateUserService(uow)
    user_dto = CreateUserDTO(**user_schema.model_dump(exclude={'password2'}))
    try:
        user = await service.execute(user_dto)
    except UserExists:
        raise HTTPException(status.HTTP_409_CONFLICT, 'User with these credentials already exists')
    else:
        return user
