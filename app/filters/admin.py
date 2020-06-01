from dataclasses import dataclass

from aiogram import types
from aiogram.dispatcher.filters.filters import BoundFilter

from app import config


@dataclass
class IsAdmin(BoundFilter):
    key = "is_admin"
    is_admin: bool

    async def check(self, message: types.Message) -> bool:
        return message.from_user.id == config.ADMIN_ID
