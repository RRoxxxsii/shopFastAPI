import asyncio
import uuid
from collections.abc import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

import src.infrastructure.database.base
from src.infrastructure.database import DATABASE_URL, get_async_session, metadata
from src.infrastructure.database.models.auth import Token, User
from src.infrastructure.database.models.item import Category, Item
from src.infrastructure.database.models.partner import Partner
from src.infrastructure.secure import pwd_context
from src.main import app

engine_test = create_async_engine(DATABASE_URL, poolclass=NullPool)
async_session_maker = async_sessionmaker(engine_test, expire_on_commit=False)
metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(autouse=True)
async def start_db():
    async with engine_test.begin() as conn:
        await conn.run_sync(src.infrastructure.database.base.AbstractModel.metadata.drop_all)
        await conn.run_sync(src.infrastructure.database.base.AbstractModel.metadata.create_all)
    # for AsyncEngine created in function scope, close and
    # clean-up pooled connections
    await engine_test.dispose()


@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


client = TestClient(app)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


def hash_pwd(pwd: str = "hashed+12345") -> str:
    return pwd_context.hash(pwd)


@pytest.fixture
async def user():
    async with async_session_maker() as session:
        user = User(
            name="name",
            surname="surname",
            email="testuser@example.com",
            hashed_password=hash_pwd(),
            is_partner=True,
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
    return user


@pytest.fixture
async def token(user):
    async with async_session_maker() as session:
        token = Token(user=user, access_token=str(uuid.uuid4()))
        session.add(token)
        await session.commit()
    return str(token)


@pytest.fixture()
async def category():
    async with async_session_maker() as session:
        category = Category(title="Shoes", description="...", data={"size": None, "color": None, "material": None})
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
            partner_id=partner.id,
        )
        session.add(item)
        await session.commit()
        await session.refresh(item)
    return item


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
