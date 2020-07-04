"""
User logic module
Specialize in user features
"""

from io import BytesIO
from typing import Tuple, Type

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State
from aiogram.utils.exceptions import PhotoDimensions

from app import config
from app.models.photo import Photo
from app.utils.httpx import HttpxWorker
from app.utils.states import UserStates

from . import base


async def get_previous_message_and_markup(
    user_states: UserStates, keyboard: dict, state_messages: dict
) -> Tuple[str, types.ReplyKeyboardMarkup]:
    """
    Get previous message and markup for `back` function

    :param user_states:     user's state obj
                            used for getting previous state
    :param keyboard:        all markups that have been added to the user's state data
    :param state_messages:  messages that are linked to the states
                            e.g. grade state    -> "Выбери клас"
                                 subject state  -> "Выбери предмет"

    :returns:               previous message and previous markup
    """

    prev_msg = None
    while not prev_msg:
        prev_state = await user_states.previous()
        prev_markup = keyboard.get(prev_state)

        if prev_markup is None:
            continue
        else:
            prev_msg = state_messages[prev_state]

    return prev_msg, prev_markup


async def set_next_state_markup(
    next_state: State,
    keyboard: dict,
    set_markup: types.ReplyKeyboardMarkup,
    state: FSMContext,
) -> None:
    """
    Set a markup to the user's next state data (concrete - `keyboard` dictionary)
    Used for `back` feature

    :param next_state:  next user's state
    :param keyboard:    contains all markups
    :param set_markup:  markup that will be set into the `keyboard` dict
    :param state:       user's state obj

    :returns:           None
    """

    keyboard[next_state.state] = set_markup.to_python()
    await base.set_state_data(state, Keyboard=keyboard)


async def send_solution_and_save_to_db(
    solution_id: int,
    solution_url: str,
    user_message: types.Message,
    photo_model: Photo,
    httpx_worker: HttpxWorker,
) -> None:
    """
    Send solution (photo) to the user and save the solution to db
    Used in `solution` handler

    :param solution_id:     solution's id
    :param solution_url:    solution's url
    :param user_message:    user's message, used for check image's
                            sizes and send the solution to the user
    :param photo_model:     photo model obj
    :param httpx_worker:    httpx obj, used for getting a solution from the solution url

    :returns:               None
    """

    photo = await base.get_model_obj_from_db_by_id(photo_model, solution_id)

    if not photo:
        img = await httpx_worker.get(solution_url)
        img_content = img.content
        img_filename = img.url.path.split("/")[-1]

        try:
            img_id = (await user_message.answer_photo(img_content)).photo[-1].file_id
        except PhotoDimensions as e:
            img_id = (
                await user_message.answer_document(
                    types.InputFile(BytesIO(img_content), filename=img_filename)
                )
            ).document.file_id
            img_id = config.PREFIX_WRONG_PHOTO_SIZE + img_id

        photo = await photo_model.create(id=solution_id, photo_id=img_id)
    else:
        img_id = photo.photo_id
        if img_id.startswith(config.PREFIX_WRONG_PHOTO_SIZE):
            await user_message.answer_document(
                img_id[len(config.PREFIX_WRONG_PHOTO_SIZE) :]
            )
        else:
            await user_message.answer_photo(img_id)
