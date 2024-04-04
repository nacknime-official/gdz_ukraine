import httpx
from aiogram import Dispatcher
from aiogram.utils.executor import Executor

# TODO: is it needed?
class HttpxClient:
    def __init__(self):
        self.client = httpx.AsyncClient(verify=False)

    async def get(self, link):
        r = await self.client.get(link)
        return r

    async def close(self):
        await self.client.aclose()


httpx_client = HttpxClient()


async def on_shutdown(dp: Dispatcher):
    await httpx_client.close()


def setup(runner: Executor):
    runner.on_shutdown(on_shutdown)
