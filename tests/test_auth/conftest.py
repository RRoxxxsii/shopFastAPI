import pytest

from src.models import User
from tests.conftest import async_session_maker


@pytest.fixture
async def user():
    async with async_session_maker() as session:
        user = User(name='name', surname='surname', email='testuser@example.com', hashed_password='hashed+12345')
        session.add(user)
        await session.commit()
    return user

