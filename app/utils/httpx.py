from aiogram import Dispatcher
from aiogram.utils.executor import Executor
import httpx


class HttpxWorker:
    def __init__(self):
        self.client = httpx.AsyncClient()

    async def get(self, link):
        r = await self.client.get(link)
        return r

    async def close(self):
        await self.client.aclose()


httpx_worker = HttpxWorker()


async def on_shutdown(dp: Dispatcher):
    await httpx_worker.close()


def setup(runner: Executor):
    runner.on_shutdown(on_shutdown)
