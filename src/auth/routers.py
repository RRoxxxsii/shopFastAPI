import re
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src import models
from src.auth import schemas
from src.database import get_async_session
from src.secure import pwd_context

router = APIRouter()


@router.post('/create-token/')
async def create_token(user: schemas.LoginUserIn, session: AsyncSession = Depends(get_async_session)):
    statement = select(models.User).where(models.User.email == user.email)
    db_user = await session.execute(statement)
    db_user = db_user.scalar_one()
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
    token = models.Token(user_id=db_user.id, access_token=str(uuid.uuid4()))
    session.add(token)
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
async def register(user: schemas.RegisterUserIn, session: AsyncSession = Depends(get_async_session)):
    hashed_password = pwd_context.hash(user.password1)
    db_user = models.User(
        name=user.name, surname=user.surname, email=user.email, hashed_password=hashed_password
    )

    session.add(db_user)
    try:
        await session.commit()
    except IntegrityError as err:
        await session.rollback()
        pattern = re.compile(r'DETAIL:\s+Key \((?P<field>.+?)\)=\((?P<value>.+?)\) already exists')
        match = pattern.search(str(err))
        raise HTTPException(
            status.HTTP_409_CONFLICT, f'User with {match['field']} {match['value']} already exists'
        )
    else:
        await session.refresh(db_user)
        return db_user
