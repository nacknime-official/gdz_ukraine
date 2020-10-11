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
from app.models.photo import Photo, Solution
from app.utils.helper import find_func_by_state_name
from app.utils.httpx import HttpxWorker
from app.utils.markups import NAVIGATION_BUTTONS, markups_list
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
        prev_markup_data = keyboard.get(prev_state)

        if prev_markup_data is None:
            continue
        else:
            prev_msg = state_messages[prev_state]

    prev_markup = find_func_by_state_name(prev_state, markups_list)(prev_markup_data)

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

    keyboard[next_state.state] = [
        j.strip() for i in set_markup.keyboard for j in i if j not in NAVIGATION_BUTTONS
    ]
    await base.set_state_data(state, Keyboard=keyboard)


async def clean_current_state_markup(
    current_state: str, keyboard: dict, state: FSMContext,
) -> None:
    """
    Clean a markup of the user's current state data (concrete - `keyboard` dictionary)
    Used for `back` feature and optimize usage of memory

    :param current_state:   current user's state
    :param keyboard:        contains all markups
    :param state:           user's state obj

    :returns:               None
    """

    del keyboard[current_state]
    await base.set_state_data(state, Keyboard=keyboard)


async def send_solution_and_save_to_db(
    solution_id: int,
    solution_url: str,
    user_message: types.Message,
    solution_model: Solution,
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
    :param solution_model:  solution model obj
    :param photo_model:     photo model obj
    :param httpx_worker:    httpx obj, used for getting a solution from the solution url

    :returns:               None
    """

    solution = await base.get_model_obj_from_db_by_id(solution_model, solution_id)
    photos = (
        await Photo.load(solution=Solution)
        .query.where(Solution.id == solution_id)
        .gino.all()
    )
    img_id = None

    if photos:
        if not (photo := photos[0]).url:
            photo.update(url=solution_url).apply()
            img_id = photo.photo_id
        else:
            for photo in photos:
                if photo.url == solution_url:
                    img_id = photo.photo_id
                    break

    if img_id is not None:
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

        if not solution:
            await solution_model.create(id=solution_id)
        await photo_model.create(
            photo_id=img_id, url=solution_url, solution_id=solution_id
        )

    else:
        if img_id.startswith(config.PREFIX_WRONG_PHOTO_SIZE):
            await user_message.answer_document(
                img_id[len(config.PREFIX_WRONG_PHOTO_SIZE) :]
            )
        else:
            await user_message.answer_photo(img_id)
