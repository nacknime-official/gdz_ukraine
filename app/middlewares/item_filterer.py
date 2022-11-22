from typing import List, Optional

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from app.services.item_filterer import ItemFilterer, ItemFiltererArgs


class ItemFiltererMiddleware(BaseMiddleware):
    def __init__(self, args: ItemFiltererArgs):
        self.item_filterer = ItemFilterer(args)
        super(ItemFiltererMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        data["item_filterer"] = self.item_filterer
