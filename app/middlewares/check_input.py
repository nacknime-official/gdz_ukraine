from typing import List

from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.storage import FSMContext

from app import config
from app.utils.helper import find_func_by_state_name
from app.utils.markups import markups_list
from app.utils.states import quiz


class Checker(BaseMiddleware):
    async def check(self, message: types.Message, state: FSMContext):
        data = await state.get_data()
        current_state = await state.get_state()
        buttons_data: List[str] = data.get("Keyboard").get(current_state)
        keyboard: types.ReplyKeyboardMarkup = find_func_by_state_name(
            current_state, markups_list
        )(buttons_data)
        buttons: List[str] = [j for i in keyboard.keyboard for j in i]
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

        if not message.is_command() and await state.get_state() in quiz:
            await self.check(message, state)
