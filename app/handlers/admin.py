import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import BotBlocked, ChatNotFound, UserDeactivated

from app import config
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
    await message.answer(text, parse_mode="html", reply_markup=markup)
    await state.update_data(Input_send_all=message.html_text)
    await AdminStates.Confirm_send_all.set()


@dp.callback_query_handler(
    lambda query: query.data == config.CB_SEND_ALL_YES,
    is_admin=True,
    state=AdminStates.Confirm_send_all,
)
async def send_all_yes(query: types.CallbackQuery, state: FSMContext):
    await query.answer()
    await query.message.edit_reply_markup()
    users = await User.select("user_id").gino.all()
    data = await state.get_data()
    text = data.get("Input_send_all")
    count = 0

    for user in users:
        try:
            await bot.send_message(user[0], text, parse_mode="html")
        except (BotBlocked, ChatNotFound, UserDeactivated) as e:
            print(e)
        else:
            count += 1
            await asyncio.sleep(0.05)

    await query.message.answer(config.MSG_SUCCESFUL_SEND_ALL.format(count))


@dp.callback_query_handler(
    lambda query: query.data == config.CB_SEND_ALL_NO,
    is_admin=True,
    state=AdminStates.Confirm_send_all,
)
async def send_all_no(query: types.CallbackQuery, state: FSMContext):
    await query.answer(text=config.MSG_DONT_WANNA)
    await query.message.edit_reply_markup()


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

    try:
        removed_message = await bot.send_message(
            user_id, "test", disable_notification=True
        )
    except BotBlocked:
        msg = "Этот юзер заблочил бота, гадёныш"
        excepted = True
    except UserDeactivated:
        msg = "Этого юзера уже нету в ТГ, банить и не нужно :)"
        excepted = True
    except ChatNotFound:
        msg = "Чат не найден, либо ты указал неверный айди, либо чел выпилился из ТГ :)"
        excepted = True
    else:
        is_blocked = (await User.get(user_id)).is_blocked
        if is_blocked:
            msg = f"{helper.get_user_link(user_id, 'Этот')} юзер и так забанен. Желаете его разбанить?"
            await state.update_data(Input_unblock=user_id)
            await AdminStates.Confirm_unblock.set()
            return await message.answer(
                msg, reply_markup=markups.confirm_unblock(), parse_mode="markdown"
            )
        else:
            msg = f"Вы уверены, что хотите забанить {helper.get_user_link(user_id)}?"
            excepted = False
        await removed_message.delete()

    if not excepted:
        await message.answer(
            msg, reply_markup=markups.confirm_block(), parse_mode="markdown"
        )
        await state.update_data(Input_block=user_id)
        await AdminStates.Confirm_block.set()
    else:
        await message.answer(msg)


@dp.callback_query_handler(
    lambda query: query.data == config.CB_BLOCK_YES,
    is_admin=True,
    state=AdminStates.Confirm_block,
)
async def block_yes(query: types.CallbackQuery, state: FSMContext):
    await query.answer()

    data = await state.get_data()
    user_id = data.get("Input_block")

    user = await User.get(user_id)
    await user.update(is_blocked=True).apply()

    await query.message.delete_reply_markup()
    await query.message.answer("Вы успешно забанили этого юзера")


@dp.callback_query_handler(
    lambda query: query.data == config.CB_UNBLOCK_YES,
    is_admin=True,
    state=AdminStates.Confirm_unblock,
)
async def unblock_yes(query: types.CallbackQuery, state: FSMContext):
    await query.answer()

    data = await state.get_data()
    user_id = data.get("Input_unblock")

    user = await User.get(user_id)
    await user.update(is_blocked=False).apply()

    await query.message.delete_reply_markup()
    await query.message.answer("Вы успешно разбанили этого юзера")


@dp.callback_query_handler(
    lambda query: query.data in (config.CB_BLOCK_NO, config.CB_UNBLOCK_NO),
    is_admin=True,
    state=[AdminStates.Confirm_block, AdminStates.Confirm_unblock],
)
async def block_unblock_no(query: types.CallbackQuery, state: FSMContext):
    await query.answer(text=config.MSG_DONT_WANNA)
    await query.message.edit_reply_markup()


# block }}}
