from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from app import config
from app.models.user import User


class ACLMiddleware(BaseMiddleware):
    async def setup_chat(self, data: dict, user: types.User, message: types.Message):
        user_id = user.id

        user = await User.get(user_id)
        if user is None:
            user = await User.create(user_id=user_id)

        if user.is_blocked:
            await message.answer(
                f"Вы заблокированы. По всем вопросам пишите {config.ADMIN_USERNAME}"
            )
            raise CancelHandler()

        data["user"] = user

    async def on_pre_process_message(self, message: types.Message, data: dict):
        await self.setup_chat(data, message.from_user, message)
