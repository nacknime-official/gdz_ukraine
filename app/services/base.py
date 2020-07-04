"""
Base logic module
Not specialize in a specific user
"""

from typing import Any

from aiogram.dispatcher import FSMContext

from app.models.db import BaseModel


async def set_state_data(state: FSMContext, **state_data) -> None:
    """
    Set data into user's state obj

    :param state:           user's state obj
    :keywords state_data    data that will be set into the state obj

    :returns:               None
    """

    await state.update_data(**state_data)


async def set_data_to_db(model: BaseModel, **data):
    """
    Set data to db through the model

    :param model:       model with which we will set data
    :keywords data:     data that will be set to db

    :returns:           None
    """

    await model.update(**data).apply()


async def get_model_obj_from_db_by_id(model: BaseModel, id: Any):
    """
    Get model object from db by id
    Used for getting solution (photo) object

    :param model:   model that contains `id` column
    :param id:      used fot getting object by id

    :returns:       model object
    """

    return await model.get(id)
