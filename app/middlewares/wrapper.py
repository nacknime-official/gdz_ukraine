from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.storage import FSMContext

from app.models.user import User
from app.utils.wrapper_vshkole import WrapperFotBot


class WrapperMiddleware(BaseMiddleware):
    async def setup_wrapper(
        self,
        data: dict,
        command,
        user: User,
        wrapper_subjects,
        wrapper_subject_entities,
        wrapper_entities,
        keyboard: dict,
    ):
        if command is None or (command is not None and command.command != "start"):
            w = WrapperFotBot(
                user,
                subjects=wrapper_subjects,
                subject_entities=wrapper_subject_entities,
                entities=wrapper_entities,
            )
            data["wrapper"] = w
            data["keyboard"] = keyboard

    async def on_process_message(self, message: types.Message, data: dict):
        command = data.get("command")
        user = data.get("user")

        state: FSMContext = data.get("state")
        state_data = await state.get_data()
        wrapper_subjects = state_data.get("Wrapper_subjects")
        wrapper_subject_entities = state_data.get("Wrapper_subject_entities")
        wrapper_entities = state_data.get("Wrapper_entities")
        keyboard: dict = state_data.get("Keyboard")
        await self.setup_wrapper(
            data,
            command,
            user,
            wrapper_subjects,
            wrapper_subject_entities,
            wrapper_entities,
            keyboard,
        )
