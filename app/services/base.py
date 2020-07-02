"""
Base logic module
Not specialize in a specific user
"""

from aiogram.dispatcher import FSMContext

from app.models.db import db


async def set_state_data(state: FSMContext, **state_data) -> None:
    """
    Set data into user's state obj

    :param state:           user's state obj
    :keywords state_data    data that will be set into the state obj

    :returns:               None
    """

    await state.update_data(**state_data)


async def set_data_to_db(model: db.Model, **data):
    """
    Set data to db through the model

    :param model:       model with which we will set data
    :keywords data:     data that will be set to db

    :returns:           None
    """

    await model.update(**data).apply()
