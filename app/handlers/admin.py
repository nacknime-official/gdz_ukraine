from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType

from app import config, services
from app.misc import bot, dp
from app.models.user import User
from app.utils import helper, markups
from app.utils.states import AdminStates


# send_all command {{{
@dp.message_handler(commands="send_all", is_admin=True, state="*")
async def cmd_send_all(message: types.Message, state: FSMContext):
    await message.answer(config.MSG_INPUT_SEND_ALL)
    await AdminStates.Input_send_all.set()


@dp.message_handler(
    content_types=ContentType.ANY, is_admin=True, state=AdminStates.Input_send_all
)
async def preview_message_send_all(message: types.Message, state: FSMContext):
    markup = markups.confirm_send_all()

    preview_sending_message = await message.copy_to(message.chat.id)
    await services.admin.set_sending_message_id(
        int(preview_sending_message.message_id), state
    )

    await message.answer(config.MSG_SEND_OR_NOT, reply_markup=markup)
    await AdminStates.Confirm_send_all.set()


@dp.callback_query_handler(
    lambda query: query.data == config.CB_SEND_ALL_YES,
    is_admin=True,
    state=AdminStates.Confirm_send_all,
)
async def send_all_yes(query: types.CallbackQuery, state: FSMContext):
    await query.answer()
    await query.message.delete_reply_markup()

    sending_message_id = await services.admin.get_sending_message_id(state)
    sending_message = types.Message(
        message_id=sending_message_id, chat=types.Chat(id=query.from_user.id)
    )
    count_alive_users = await services.admin.send_all(
        sending_message=sending_message, user_model=User
    )
    await query.message.answer(config.MSG_SUCCESSFUL_SEND_ALL.format(count_alive_users))


@dp.callback_query_handler(
    lambda query: query.data == config.CB_SEND_ALL_NO,
    is_admin=True,
    state=AdminStates.Confirm_send_all,
)
async def send_all_no(query: types.CallbackQuery, state: FSMContext):
    await query.answer(text=config.MSG_DONT_WANNA)
    await query.message.delete_reply_markup()


@dp.message_handler(commands="count_alive_users", is_admin=True, state="*")
async def cmd_count_alive_users(message: types.Message, state: FSMContext):
    count_alive_users = await services.admin.send_all(bot=bot, user_model=User)
    await message.answer(config.MSG_SUCCESSFUL_SEND_ALL.format(count_alive_users))


# end send_all command }}}

# block {{{
@dp.message_handler(commands="block", is_admin=True, state="*")
async def cmd_block(message: types.Message):
    await message.answer(config.MSG_INPUT_BLOCKING_USER_ID)
    await AdminStates.Input_block.set()


@dp.message_handler(is_admin=True, state=AdminStates.Input_block)
async def block_confirm(message: types.Message, state: FSMContext):
    user_id = message.text
    if not user_id.isdigit():
        await message.answer(config.MSG_WRONG_BLOCKING_USER_ID)
        return
    user_id = int(user_id)

    is_blocked = await services.admin.is_user_blocked(user_id, User)
    if is_blocked:
        msg = f"{helper.get_user_link(user_id, config.MSG_THIS_USER)} {config.MSG_USER_ALREADY_BLOCKED_DO_YOU_WANNA_UNBLOCK}"
        await message.answer(
            msg, reply_markup=markups.confirm_unblock(), parse_mode="markdown"
        )
        await services.admin.set_unblocking_user_id(user_id, state)
        await AdminStates.Confirm_unblock.set()
    else:
        error = await services.admin.check_user_alive(bot, user_id)

        if error:
            return await message.answer(error)

        msg = f"{config.MSG_BLOCK_SURE} {helper.get_user_link(user_id)}?"
        await message.answer(
            msg, reply_markup=markups.confirm_block(), parse_mode="markdown"
        )
        await services.admin.set_blocking_user_id(user_id, state)
        await AdminStates.Confirm_block.set()


@dp.callback_query_handler(
    lambda query: query.data == config.CB_BLOCK_YES,
    is_admin=True,
    state=AdminStates.Confirm_block,
)
async def block_yes(query: types.CallbackQuery, state: FSMContext):
    await query.answer()

    blocking_user_id = await services.admin.get_blocking_user_id(state)
    await services.admin.block_user(blocking_user_id, User)

    await query.message.delete_reply_markup()
    await query.message.answer(config.MSG_SUCCESSFUL_BLOCK)


@dp.callback_query_handler(
    lambda query: query.data == config.CB_UNBLOCK_YES,
    is_admin=True,
    state=AdminStates.Confirm_unblock,
)
async def unblock_yes(query: types.CallbackQuery, state: FSMContext):
    await query.answer()

    unblocking_user_id = await services.admin.get_unblocking_user_id(state)
    await services.admin.unblock_user(unblocking_user_id, User)

    await query.message.delete_reply_markup()
    await query.message.answer(config.MSG_SUCCESSFUL_UNBLOCK)


@dp.callback_query_handler(
    lambda query: query.data in (config.CB_BLOCK_NO, config.CB_UNBLOCK_NO),
    is_admin=True,
    state=[AdminStates.Confirm_block, AdminStates.Confirm_unblock],
)
async def block_unblock_no(query: types.CallbackQuery):
    await query.answer(text=config.MSG_DONT_WANNA)
    await query.message.delete_reply_markup()


# block }}}

# notifications {{{
@dp.message_handler(commands="toggle_notifs", is_admin=True, state="*")
async def toggle_user_is_subscribed_to_notifications(
    message: types.Message, state: FSMContext
):
    user_id = message.text.split()[-1]
    if not user_id.isdigit():
        await message.answer(config.MSG_WRONG_TOGGLE_NOTIFS_USER_ID)
        return
    user_id = int(user_id)

    error = await services.admin.check_user_alive(bot, user_id)

    if error:
        return await message.answer(error)

    is_subscribed_to_notifications = (
        await services.admin.is_user_subscribed_to_notifications(
            user_id=user_id,
            user_model=User,
        )
    )
    toggle_service = (
        services.admin.unsubscribe_user_to_notifications
        if is_subscribed_to_notifications
        else services.admin.subscribe_user_to_notifications
    )
    msg = await toggle_service(
        user_id=user_id,
        user_model=User,
    )
    await message.answer(msg)


@dp.message_handler(commands="send_notifs", is_admin=True, state="*")
async def cmd_send_notifs(message: types.Message):
    await message.answer(config.MSG_INPUT_SEND_NOTIFS)
    await AdminStates.Input_send_notifs.set()


@dp.message_handler(
    content_types=ContentType.ANY, is_admin=True, state=AdminStates.Input_send_notifs
)
async def preview_message_send_notifs(message: types.Message, state: FSMContext):
    markup = markups.confirm_send_notifs()

    preview_sending_message = await message.copy_to(message.chat.id)
    await services.admin.set_sending_message_id(
        int(preview_sending_message.message_id), state
    )

    await message.answer(config.MSG_SEND_OR_NOT, reply_markup=markup)
    await AdminStates.Confirm_send_notifs.set()


@dp.callback_query_handler(
    lambda query: query.data == config.CB_SEND_NOTIFS_YES,
    is_admin=True,
    state=AdminStates.Confirm_send_notifs,
)
async def send_notifs_yes(query: types.CallbackQuery, state: FSMContext):
    await query.answer()
    await query.message.delete_reply_markup()

    sending_message_id = await services.admin.get_sending_message_id(state)
    sending_message = types.Message(
        message_id=sending_message_id, chat=types.Chat(id=query.from_user.id)
    )
    count_alive_users = await services.admin.send_notifs(
        sending_message=sending_message, user_model=User
    )
    await query.message.answer(
        config.MSG_SUCCESSFUL_SEND_NOTIFS.format(count_alive_users)
    )


@dp.callback_query_handler(
    lambda query: query.data == config.CB_SEND_NOTIFS_NO,
    is_admin=True,
    state=AdminStates.Confirm_send_notifs,
)
async def send_notifs_no(query: types.CallbackQuery):
    await query.answer(text=config.MSG_DONT_WANNA)
    await query.message.delete_reply_markup()


# notifications }}}
