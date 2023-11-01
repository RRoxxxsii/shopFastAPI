import pytest

from src.models import User
from src.secure import pwd_context
from tests.conftest import async_session_maker


def hash_pwd(pwd: str = 'hashed+12345') -> str:
    return pwd_context.hash(pwd)


@pytest.fixture(scope='session')
async def user():
    async with async_session_maker() as session:
        user = User(name='name', surname='surname', email='testuser@example.com', hashed_password=hash_pwd())
        session.add(user)
        await session.commit()
    return user

