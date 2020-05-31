from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from app.models.user import User


class ACLMiddleware(BaseMiddleware):
    async def setup_chat(self, data: dict, user: types.User):
        user_id = user.id

        user = await User.get(user_id)
        if user is None:
            user = await User.create(user_id=user_id)

        data["user"] = user

    async def on_pre_process_message(self, message: types.Message, data: dict):
        await self.setup_chat(data, message.from_user)
