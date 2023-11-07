import asyncio
import re
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.database import get_async_session
from src.models import Seller
from src.partners import schemas
from src.partners.validate_api import validate
from src.secure import apikey_scheme
from src.users import get_user_by_token

router = APIRouter()


@router.post('/register-as-seller/')
def become_partner_no_account():
    """
    Create account for the first times as partner,
    when no account for the same user with same
    credentials in common does not exist
    """
    pass


@router.post('/upgrade-to-seller/', response_model=schemas.SellerOut, status_code=status.HTTP_201_CREATED)
async def become_partner_exist_account(
        seller: schemas.SellerIn,
        access_token: Annotated[str, Depends(apikey_scheme)],
        session: AsyncSession = Depends(get_async_session)
):
    trrc = seller.trrc
    bic = seller.bic
    tin = seller.tin
    mobile = seller.mobile

    trrc_valid, bic_valid, tin_valid, mobile_valid = await asyncio.gather(
        validate(f'https://htmlweb.ru/api.php?obj=validator&m=kpp&kpp={trrc}'),
        validate(f'https://htmlweb.ru/api.php?obj=validator&m=bic&bic={bic}'),
        validate(f'https://htmlweb.ru/api.php?obj=validator&m=inn&inn={tin}'),
        validate(f'https://htmlweb.ru/api.php?obj=validator&m=phone&phone={mobile}')
    )
    if not all((trrc_valid, bic_valid, tin_valid, mobile_valid)):
        raise HTTPException(
            status.HTTP_409_CONFLICT, 'Credentials are not valid'
        )
    user = await get_user_by_token(token=access_token, session=session)
    seller = Seller(
        user=user, bic=bic, trrc=trrc, mobile=mobile, an=seller.an,
        bank_name=seller.bank_name, company_name=seller.company_name,
        company_description=seller.company_description,
        additional=seller.additional, tin=seller.tin, passport_scan='a',
        tc_scan='a'
    )

    session.add(seller)
    try:
        await session.commit()
    except IntegrityError as err:
        await session.rollback()
        pattern = re.compile(r'DETAIL:\s+Key \((?P<field>.+?)\)=\((?P<value>.+?)\) already exists')
        match = pattern.search(str(err))
        raise HTTPException(
            status.HTTP_409_CONFLICT, f'User with {match["field"]} {match["value"]} already exists'
        )
    else:
        await session.refresh(seller)
        return seller
