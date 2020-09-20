"""
Admin logic module
Specialize in admin features
"""

import asyncio
import typing

from aiogram import Bot, types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import BotBlocked, ChatNotFound, UserDeactivated

from app.models.user import User

from . import base


async def send_message_catching_errors(
    bot: Bot,
    chat_id: typing.Union[types.base.Integer, types.base.String],
    text: types.base.String,
    parse_mode: typing.Union[types.base.String, None] = None,
    disable_web_page_preview: typing.Union[types.base.Boolean, None] = None,
    disable_notification: typing.Union[types.base.Boolean, None] = None,
    reply_to_message_id: typing.Union[types.base.Integer, None] = None,
    reply_markup: typing.Union[
        types.InlineKeyboardMarkup,
        types.ReplyKeyboardMarkup,
        types.ReplyKeyboardRemove,
        types.ForceReply,
        None,
    ] = None,
) -> typing.Tuple[types.Message, str]:
    """
    Send a message catching errors e.g. BotBlocked, UserDeactivated, ChatNotFound etc.
    Used as abstract method

    :param bot:     bot object
    :other params:  for aiogram.Bot.send_message method

    :returns:       types.Message obj and an error
    """

    message = None
    error = ""

    try:
        message = await bot.send_message(
            chat_id,
            text,
            parse_mode=parse_mode,
            disable_web_page_preview=disable_web_page_preview,
            disable_notification=disable_notification,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup,
        )
    except BotBlocked:
        error = "Этот юзер заблочил бота, гадёныш"
    except UserDeactivated:
        error = "Этого юзера уже нету в ТГ, банить и не нужно :)"
    except ChatNotFound:
        error = (
            "Чат не найден, либо ты указал неверный айди, либо чел выпилился из ТГ :)"
        )

    return message, error


async def set_sending_text(sending_text: str, state: FSMContext) -> None:
    """
    Set sending text into admin's state data for getting that later in the next handler

    :param state:   admin's state obj in which we'll set sending text

    :returns:       None
    """

    await base.set_state_data(state, Input_send_all=sending_text)


async def get_sending_text(state: FSMContext) -> str:
    """
    Get sending text to the all users from the admin's state obj

    :param state:   admin's state obj that contains sending text

    :returns:       sending text
    """

    data = await state.get_data()
    sending_text = data.get("Input_send_all")

    return sending_text


async def send_all(
    bot: Bot, *, sending_text: typing.Optional[str] = None, user_model: User
) -> int:
    """
    Sends the message for all users
    It's only admin's feature

    :param bot:             bot obj
    :param sending_text:    text that will be sent to the all users
                            if there's no text, it's silent broadcast with
                            deleting message for count alive users
    :param user_model:      user's model for getting all user's id

    :returns:               `count_alive_users` var
    """

    all_users_id = await user_model.select("user_id").gino.all()
    count_alive_users = 0

    for user_id in all_users_id:
        if sending_text:
            message, error = await send_message_catching_errors(
                bot, user_id[0], sending_text, parse_mode="html"
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
    await base.set_data_to_db(user_model, is_blocked=True)

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
    await base.set_data_to_db(user_model, is_blocked=False)

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
        bot, user_id, "test", disable_notification=True
    )
    if not error:
        await removed_message.delete()

    return error
