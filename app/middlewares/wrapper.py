from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.storage import FSMContext

from app.models.user import User
from app.services.wrappers.wrapper_vshkole import WrapperVshkole, create_wrapper_vshkole_for_bot
from app.utils.httpx import httpx_client


class WrapperMiddleware(BaseMiddleware):
    async def setup_wrapper(
        self,
        data: dict,
        command,
        user: User,
        state: FSMContext,
        keyboard: dict,
    ):
        if command is None or (command is not None and command.command != "start"):
            w = await create_wrapper_vshkole_for_bot(
                WrapperVshkole(client=httpx_client), user, state
            )
            data["wrapper"] = w
            data["keyboard"] = keyboard

    async def on_process_message(self, message: types.Message, data: dict):
        command = data.get("command")
        user = data.get("user")

        state: FSMContext = data.get("state")
        state_data: dict = await state.get_data()
        keyboard: dict = state_data.get("Keyboard")
        await self.setup_wrapper(
            data,
            command,
            user,
            state,
            keyboard,
        )
