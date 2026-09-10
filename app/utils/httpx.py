import httpx
from aiogram import Dispatcher
from aiogram.utils.executor import Executor

BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/128.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "gzip, deflate",
    "Sec-Ch-Ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "Referer": "https://vshkole.com/",
}


# TODO: is it needed?
class HttpxClient:
    def __init__(self):
        self.client = httpx.AsyncClient(
            headers=BROWSER_HEADERS,
            verify=False,
        )

    async def get(self, link):
        r = await self.client.get(link)
        print(r.text)
        return r

    async def close(self):
        await self.client.aclose()


httpx_client = HttpxClient()


async def on_shutdown(dp: Dispatcher):
    await httpx_client.close()


def setup(runner: Executor):
    runner.on_shutdown(on_shutdown)
