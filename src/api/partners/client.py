import asyncio

from src.api.partners.validate import APICall


class Client:

    async def call(self, *args):
        res = await asyncio.gather(*(APICall.validate(url) for url in args))
        return all(res)
