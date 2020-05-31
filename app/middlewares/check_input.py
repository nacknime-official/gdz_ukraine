from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.storage import FSMContext

from app import config
from app.utils.states import quiz


class Checker(BaseMiddleware):
    async def check(self, message: types.Message, state: FSMContext):
        data = await state.get_data()
        current_state = await state.get_state()
        keyboard: dict = data.get("Keyboard").get(current_state)
        keyboard: types.ReplyKeyboardMarkup = types.ReplyKeyboardMarkup.to_object(
            keyboard
        )
        buttons = [j for i in keyboard.keyboard for j in i]
        text = message.text

        if text[-1] == "…":
            for button in buttons:
                if button.startswith(text[:-1]):
                    text = button
                    break

        if text not in buttons:
            await message.answer(config.MSG_WRONG_INPUT)
            raise CancelHandler()

    async def on_process_message(self, message: types.Message, data: dict):
        state = data.get("state")

        if (
            message.get_command() not in config.ADMIN_COMMANDS
            and await state.get_state() in quiz
        ):
            await self.check(message, state)
