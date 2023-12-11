import aiohttp
import pytest

from src.infrastructure.database.models.auth import User
from src.infrastructure.database.models.item import Category, Item
from src.infrastructure.database.models.partner import Partner
from tests.conftest import async_session_maker, hash_pwd


@pytest.fixture(scope="session", autouse=True)
async def httpsession():
    async with aiohttp.ClientSession(trust_env=True):
        yield


@pytest.fixture()
async def partner(user):
    async with async_session_maker() as session:

        seller = Partner(
            user=user,
            mobile="88005553535",
            company_name="Name",
            company_description="Description",
            bank_name="Sber",
            tin="381111467850",
            bic="044525225",
            trrc="775001001",
            an="783768329692",
            is_approved=True,
        )
        session.add(seller)
        await session.commit()
        await session.refresh(seller)
    return seller


@pytest.fixture()
async def category():
    async with async_session_maker() as session:
        category = Category(
            title='Shoes',
            description='...',
            data={'size': None, 'color': None, 'material': None}
        )
        session.add(category)
        await session.commit()
        await session.refresh(category)
    return category


@pytest.fixture()
async def item(category, partner):
    async with async_session_maker() as session:
        item = Item(
            title="Iphone 15 Pro Max",
            description="Cool phone",
            price=1.2,
            category_id=category.id,
            data={"size": "42", "color": "red", "material": "leather"},
            partner_id=partner.id
        )
        session.add(item)
        await session.commit()
        await session.refresh(item)
    return item
