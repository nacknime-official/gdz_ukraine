"""
Admin logic module
Specialize in admin features
"""

import asyncio
import typing

from aiogram import Bot, types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import BotBlocked, ChatNotFound, UserDeactivated

from app import config
from app.models.user import User

from . import base


async def send_message_catching_errors(
    chat_id: typing.Union[types.base.Integer, types.base.String],
    message: types.Message,
    bot: typing.Optional[Bot] = None,
) -> typing.Tuple[types.Message, str]:
    """
    Send a message catching errors e.g. BotBlocked, UserDeactivated, ChatNotFound etc.
    Used as abstract method

    :param bot:     bot object
    :other params:  for aiogram.Bot.send_message method

    :returns:       types.Message obj and an error
    """

    error = ""

    try:
        # if message is created by the code
        if not message.message_id:
            message = await bot.send_message(chat_id=chat_id, **message.to_python())
        else:
            await message.copy_to(chat_id)
    except BotBlocked:
        error = "Этот юзер заблочил бота"
    except UserDeactivated:
        error = "Этого юзера уже нету в ТГ"
    except ChatNotFound:
        error = "Чат не найден, либо чел выпилился из ТГ"

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


async def send_all(
    *,
    sending_message: typing.Optional[types.Message] = None,
    bot: typing.Optional[Bot] = None,
    user_model: typing.Type[User]
) -> int:
    """
    Sends the message for all users
    It's only admin's feature

    :param message:         message that will be sent to the all users
                            if there's no message, it's silent broadcast with
                            deleting message for count alive users
    :param bot:             bot obj
    :param user_model:      user's model for getting all user's id

    :returns:               `count_alive_users` var
    """

    all_users_id = await user_model.select("user_id").gino.all()
    count_alive_users = 0

    for user_id in all_users_id:
        if sending_message:
            message, error = await send_message_catching_errors(
                user_id[0], sending_message, bot=bot
            )
        else:
            error = await check_user_alive(bot, user_id[0])
        if not error:
            count_alive_users += 1
            await asyncio.sleep(0.05)

    return count_alive_users


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

    removed_message, error = await send_message_catching_errors(
        user_id, types.Message(text="test", disable_notification=True), bot=bot
    )
    if not error:
        await removed_message.delete()

    return error


async def scheduled_count_alive_users(bot: Bot, user_model: typing.Type[User]):
    """
    Count alive users used with systemd or crontab
    """

    await bot.send_message(
        config.ADMIN_ID, "Запланированная рассылка для подсчёта юзеров начата"
    )

    count_alive_users = await send_all(bot=bot, user_model=user_model)
    await bot.send_message(
        config.ADMIN_ID, config.MSG_SUCCESFUL_SEND_ALL.format(count_alive_users)
    )
