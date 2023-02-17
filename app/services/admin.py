"""
Admin logic module
Specialize in admin features
"""

import asyncio
import typing

from aiogram import Bot, types
from aiogram.dispatcher import FSMContext
from aiogram.types.chat import ChatActions
from sqlalchemy.util import counter

from app import config
from app.models.db import db
from app.models.user import User
from app.utils.exceptions import (
    UserIsNotWithUsException,
    catch_user_is_not_with_us_exceptions,
)

from . import base


async def send_message_catching_errors(
    chat_id: typing.Union[types.base.Integer, types.base.String],
    message: types.Message,
) -> typing.Tuple[types.Message, str]:
    """
    Send a message catching errors e.g. BotBlocked, UserDeactivated, ChatNotFound etc.
    Used as abstract method

    :other params:  for aiogram.Bot.send_message method

    :returns:       types.Message obj and an error
    """

    error = ""

    try:
        with catch_user_is_not_with_us_exceptions():
            await message.copy_to(chat_id)
    except UserIsNotWithUsException as e:
        error = e.error_message

    return message, error


async def set_sending_message_id(message_id: int, state: FSMContext) -> None:
    """
    Set sending message id into admin's state data for getting that later in the next handler

    :param state:   admin's state obj in which we'll set sending message id

    :returns:       None
    """

    await base.set_state_data(state, Input_send_all=message_id)


async def get_sending_message_id(state: FSMContext) -> str:
    """
    Get sending message id to the all users from the admin's state obj

    :param state:   admin's state obj that contains sending message id

    :returns:       sending text
    """

    data = await state.get_data()
    sending_message_id = data.get("Input_send_all")

    return sending_message_id


async def send_messages_counting_alive_users(
    *,
    sending_message: typing.Optional[types.Message],
    users_ids: typing.List[typing.List[int]],
) -> int:
    """
    :param message:         message that will be sent to the users
    :param user_model:      user's model for getting all user's id

    :returns:               `count_alive_users` var
    """
    count_alive_users = 0

    for user_id in users_ids:
        _, error = await send_message_catching_errors(user_id[0], sending_message)
        if not error:
            count_alive_users += 1
            await asyncio.sleep(0.05)

    return count_alive_users


async def send_all(
    *,
    sending_message: typing.Optional[types.Message],
    user_model: typing.Type[User],
) -> int:
    """
    Sends the message for all users.
    It's only admin's feature

    :param message:         message that will be sent to the all users
    :param user_model:      user's model for getting all user's id

    :returns:               `count_alive_users` var
    """

    all_users_ids = await user_model.select("user_id").gino.all()
    return await send_messages_counting_alive_users(
        sending_message=sending_message,
        users_ids=all_users_ids,
    )


async def send_notifs(
    *,
    sending_message: typing.Optional[types.Message],
    user_model: typing.Type[User],
) -> int:
    """
    Sends the message for all users, except for those unsubscribed to notifications.
    It's only admin's feature

    :param message:         message that will be sent to the users
    :param user_model:      user's model for getting all user's id

    :returns:               `count_alive_users` var
    """

    subscribed_to_notifications_users_ids = await (
        user_model.select("user_id")
        .where(user_model.is_subscribed_to_notifications == True)
        .gino.all()
    )
    return await send_messages_counting_alive_users(
        sending_message=sending_message,
        users_ids=subscribed_to_notifications_users_ids,
    )


async def set_blocking_user_id(
    blocking_user_id: typing.Union[int, str], state: FSMContext
) -> None:
    """
    Set blocking user's id into admin's state data for getting that later in the next handler

    :param state:   admin's state obj in which we'll set user's id

    :returns:       None
    """

    blocking_user_id = int(blocking_user_id)
    await base.set_state_data(state, Input_block=blocking_user_id)


async def get_blocking_user_id(state: FSMContext) -> int:
    """
    Get blocking user's id from the admin's state obj

    :param state:   admin's state that contains user's id

    :returns:       user's id
    """

    data = await state.get_data()
    blocking_user_id = data.get("Input_block")

    return blocking_user_id


async def set_unblocking_user_id(
    unblocking_user_id: typing.Union[int, str], state: FSMContext
) -> None:
    """
    Set unblocking user's id into admin's state data for getting that later in the next handler

    :param state:   admin's state obj in which we'll set user's id

    :returns:       None
    """

    unblocking_user_id = int(unblocking_user_id)
    await base.set_state_data(state, Input_unblock=unblocking_user_id)


async def get_unblocking_user_id(state: FSMContext) -> int:
    """
    Get unblocking user's id from the admin's state obj

    :param state:   admin's state that contains user's id

    :returns:       user's id
    """

    data = await state.get_data()
    unblocking_user_id = data.get("Input_unblock")

    return unblocking_user_id


async def block_user(user_id: typing.Union[int, str], user_model: User) -> User:
    """
    Blocks the user

    :param user_id:     user's id that will be blocked
    :param user_model:  user's model for getting user from DB

    :returns:           user's model obj
    """

    user_id = int(user_id)
    user = await user_model.get(user_id)
    await base.set_data_to_db(user, is_blocked=True)

    return user


async def unblock_user(user_id: typing.Union[int, str], user_model: User) -> User:
    """
    Unblocks the user

    :param user_id:     user's id that will be unblocked
    :param user_model:  user's model for getting user from DB

    :returns:           user's model obj
    """

    user_id = int(user_id)
    user = await user_model.get(user_id)
    await base.set_data_to_db(user, is_blocked=False)

    return user


async def is_user_blocked(user_id: typing.Union[int, str], user_model: User) -> bool:
    """
    Is user already blocked or not

    :param user_id:     user's id
    :param user_model:  user's model for getting user from DB

    :returns:           is user blocked
    """

    user_id = int(user_id)
    is_blocked = (await user_model.get(user_id)).is_blocked

    return is_blocked


async def check_user_alive(
    bot: Bot, user_id: typing.Union[int, str]
) -> typing.Union[str]:
    """
    Check if the user hasn't blocked the bot, user is banned etc.
    or is the user alive

    :param bot:         bot obj
    :param user_id:     user's id that will be checked

    :returns:           error message
    """

    error = ""
    try:
        with catch_user_is_not_with_us_exceptions():
            await bot.send_chat_action(user_id, ChatActions.TYPING)
    except UserIsNotWithUsException as e:
        error = e.error_message

    return error


async def count_alive_users(bot: Bot, user_model: typing.Type[User]) -> int:
    """
    Count alive users

    :param bot:         bot obj
    :param user_model:  user's model for getting user from DB

    :returns:           count of alive users
    """

    count_alive_users = 0

    async with db.transaction():
        async for user_id in user_model.select("user_id").gino.iterate():
            user_id = user_id[0]

            error = await check_user_alive(bot, user_id)
            if not error:
                count_alive_users += 1
                await asyncio.sleep(0.05)

    return count_alive_users


async def count_alive_users_and_send_result(
    bot: Bot, to_user_id: typing.Union[int, str], user_model: typing.Type[User]
):
    """
    Count alive users and send result to user with `to_user_id` id

    :param bot:         bot obj
    :param to_user_id:  user's id
    :param user_model:  user's model for getting user from DB

    :returns:           count of alive users
    """

    await bot.send_message(to_user_id, config.MSG_BEGIN_COUNTING_ALIVE_USERS)
    res = await count_alive_users(bot=bot, user_model=User)
    await bot.send_message(to_user_id, config.MSG_END_COUNTING_ALIVE_USERS.format(res))


async def is_user_subscribed_to_notifications(
    user_id: typing.Union[int, str], user_model: User
) -> bool:
    """
    Is user subscribed to notifications (like "Happy New Year!")

    :param user_id:     user's id
    :param user_model:  user's model for getting user from DB

    :returns:           is user subscribed to notifications
    """

    user_id = int(user_id)
    is_subscribed_to_notifications = (
        await user_model.get(user_id)
    ).is_subscribed_to_notifications

    return is_subscribed_to_notifications


async def subscribe_user_to_notifications(
    user_id: typing.Union[int, str],
    user_model: typing.Type[User],
):
    user_id = int(user_id)
    user = await user_model.get(user_id)
    await user.update(is_subscribed_to_notifications=True).apply()

    return "Юзер был подписан"


async def unsubscribe_user_to_notifications(
    user_id: typing.Union[int, str],
    user_model: typing.Type[User],
):
    user_id = int(user_id)
    user = await user_model.get(user_id)
    await user.update(is_subscribed_to_notifications=False).apply()

    return "Юзер был отписан"
