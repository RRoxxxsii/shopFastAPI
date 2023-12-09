import aiohttp
import pytest

from src.infrastructure.database.models.auth import User
from src.infrastructure.database.models.partner import Partner
from tests.conftest import async_session_maker, hash_pwd


@pytest.fixture(scope='session', autouse=True)
async def httpsession():
    async with aiohttp.ClientSession(trust_env=True):
        yield


@pytest.fixture()
async def seller():
    async with async_session_maker() as session:
        user = User(
            name='name', surname='surname', email='email@gmail.com', hashed_password=hash_pwd()
        )

        seller = Partner(
            user=user, mobile='88005553535', company_name='Name', company_description='Description',
            bank_name='Sber', tin='381111467850', bic='044525225', trrc='775001001', an='783768329692'
        )
        session.add_all([user, seller])
        await session.commit()
    return seller
