import re

import bcrypt
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src import models
from src.auth import schemas
from src.database import get_async_session


router = APIRouter()


@router.post('/sign-up/', response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED,
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
async def register(user: schemas.UserIn, session: AsyncSession = Depends(get_async_session)):
    encoded_password = user.password1.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = str(bcrypt.hashpw(encoded_password, salt))
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
