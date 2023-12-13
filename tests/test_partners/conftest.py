import aiohttp
import pytest


@pytest.fixture(scope="session", autouse=True)
async def httpsession():
    async with aiohttp.ClientSession(trust_env=True):
        yield
