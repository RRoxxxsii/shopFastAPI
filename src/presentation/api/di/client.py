import aiohttp

from src.infrastructure.api_client.partners.implementation import Client


def get_aiohttp_client():
    return Client(aiohttp.ClientSession)
