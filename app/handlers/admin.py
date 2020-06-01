import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import BotBlocked, ChatNotFound

from app import config
from app.misc import bot, dp
from app.models.user import User
from app.utils import markups
from app.utils.states import AdminStates


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
        except (BotBlocked, ChatNotFound) as e:
            print(e)
        else:
            count += 1
            await asyncio.sleep(0.7)

    await query.message.answer(config.MSG_SUCCESFUL_SEND_ALL.format(count))


@dp.callback_query_handler(
    lambda query: query.data == config.CB_SEND_ALL_NO,
    is_admin=True,
    state=AdminStates.Confirm_send_all,
)
async def send_all_no(query: types.CallbackQuery, state: FSMContext):
    await query.answer(text=config.MSG_DONT_WANNA_SEND_ALL)
    await query.message.edit_reply_markup()
