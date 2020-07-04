import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import BotBlocked, ChatNotFound, UserDeactivated

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


@dp.message_handler(is_admin=True, state=AdminStates.Input_send_all)
async def preview_message_send_all(message: types.Message, state: FSMContext):
    markup = markups.confirm_send_all()
    text = f"""
{message.html_text}

Отправить?
"""
    await services.admin.set_sending_text(message.html_text, state)
    await message.answer(text, parse_mode="html", reply_markup=markup)
    await AdminStates.Confirm_send_all.set()


@dp.callback_query_handler(
    lambda query: query.data == config.CB_SEND_ALL_YES,
    is_admin=True,
    state=AdminStates.Confirm_send_all,
)
async def send_all_yes(query: types.CallbackQuery, state: FSMContext):
    await query.answer()
    await query.message.delete_reply_markup()

    sending_text = await services.admin.get_sending_text(state)
    count_alive_users = await services.admin.send_all(bot, sending_text, User)
    await query.message.answer(config.MSG_SUCCESFUL_SEND_ALL.format(count_alive_users))


@dp.callback_query_handler(
    lambda query: query.data == config.CB_SEND_ALL_NO,
    is_admin=True,
    state=AdminStates.Confirm_send_all,
)
async def send_all_no(query: types.CallbackQuery, state: FSMContext):
    await query.answer(text=config.MSG_DONT_WANNA)
    await query.message.delete_reply_markup()


# end send_all command }}}

# block {{{
@dp.message_handler(commands="block", is_admin=True, state="*")
async def cmd_block(message: types.Message):
    await message.answer("Введите айди юзера, которого нужно забанить")
    await AdminStates.Input_block.set()


@dp.message_handler(is_admin=True, state=AdminStates.Input_block)
async def block_confirm(message: types.Message, state: FSMContext):
    user_id = message.text
    if not user_id.isdigit():
        await message.answer("Это не айдишник юзера, попробуй ещё раз, но с числами")
        return
    user_id = int(user_id)

    is_blocked = await services.admin.is_user_blocked(user_id, User)
    if is_blocked:
        msg = f"{helper.get_user_link(user_id, 'Этот')} юзер и так забанен. Желаете его разбанить?"
        await message.answer(
            msg, reply_markup=markups.confirm_unblock(), parse_mode="markdown"
        )
        await services.admin.set_unblocking_user_id(user_id, state)
        await AdminStates.Confirm_unblock.set()
    else:
        error = await services.admin.check_user_alive(bot, user_id)

        if error:
            return await message.answer(error)

        msg = f"Вы уверены, что хотите забанить {helper.get_user_link(user_id)}?"
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
    await query.message.answer("Вы успешно забанили этого юзера")


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
    await query.message.answer("Вы успешно разбанили этого юзера")


@dp.callback_query_handler(
    lambda query: query.data in (config.CB_BLOCK_NO, config.CB_UNBLOCK_NO),
    is_admin=True,
    state=[AdminStates.Confirm_block, AdminStates.Confirm_unblock],
)
async def block_unblock_no(query: types.CallbackQuery, state: FSMContext):
    await query.answer(text=config.MSG_DONT_WANNA)
    await query.message.delete_reply_markup()


# block }}}
