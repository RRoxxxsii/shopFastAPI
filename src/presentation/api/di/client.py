import aiohttp
from src.infrastructure.api_client.partners.implementation import Client


def get_aiohttp_session():
    return Client(aiohttp.ClientSession)
