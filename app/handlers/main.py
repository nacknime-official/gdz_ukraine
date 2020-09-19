from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import PhotoDimensions

from app import config, services
from app.misc import dp
from app.models.photo import Photo
from app.models.user import User
from app.utils import markups
from app.utils.helper import find_func_by_state_name
from app.utils.httpx import httpx_worker
from app.utils.states import UserStates, quiz, state_messages
from app.utils.wrapper_vshkole import WrapperForBot, data_funcs


@dp.message_handler(text="Назад", state=quiz)
async def back(
    message: types.Message,
    user: User,
    wrapper: WrapperForBot,
    keyboard: dict,
    state: FSMContext,
):
    await services.user.clean_current_state_markup(
        await state.get_state(), keyboard, state
    )

    wrapper_func = find_func_by_state_name(await state.get_state(), data_funcs)
    await wrapper_func(wrapper, delete_data=True)

    prev_msg, prev_markup = await services.user.get_previous_message_and_markup(
        UserStates, keyboard, state_messages
    )
    await message.answer(prev_msg, reply_markup=prev_markup)


@dp.message_handler(text="Главное меню", state="*")
@dp.message_handler(commands="start", state="*")
async def cmd_start(message: types.Message, user: User, state: FSMContext):
    await state.reset_data()

    markup = markups.classes()
    await message.answer(config.MSG_START, reply_markup=markup)

    keyboard: dict = {}
    next_state = UserStates.Grade
    await next_state.set()
    await services.user.set_next_state_markup(next_state, keyboard, markup, state)


@dp.message_handler(lambda message: message.is_command(), state="*")
async def cmd_any(message: types.Message, user: User, state: FSMContext):
    await message.answer("Такой команды нету")


@dp.message_handler(state=UserStates.Grade)
async def subject(
    message: types.Message,
    user: User,
    wrapper: WrapperForBot,
    keyboard: dict,
    state: FSMContext,
):
    grade = int(message.text)
    await services.base.set_data_to_db(user, grade=grade)

    subjects = await wrapper.subjects()
    subjects_name = [subject["name"] for subject in subjects]
    markup = markups.subjects(subjects_name)
    await message.answer(config.MSG_SUBJECT, reply_markup=markup)

    next_state = UserStates.Subject
    await next_state.set()
    await services.user.set_next_state_markup(next_state, keyboard, markup, state)


@dp.message_handler(state=UserStates.Subject)
async def author(
    message: types.Message,
    user: User,
    wrapper: WrapperForBot,
    keyboard: dict,
    state: FSMContext,
):
    subject = message.text
    await services.base.set_data_to_db(user, subject=subject)

    authors = await wrapper.authors()
    markup = markups.authors(authors)
    await message.answer(config.MSG_AUTHOR, reply_markup=markup)

    next_state = UserStates.Author
    await next_state.set()
    await services.user.set_next_state_markup(next_state, keyboard, markup, state)


@dp.message_handler(state=UserStates.Author)
async def specifications(
    message: types.Message,
    user: User,
    wrapper: WrapperForBot,
    keyboard: dict,
    state: FSMContext,
):
    author = message.text
    await services.base.set_data_to_db(user, author=author)

    specifications = await wrapper.specifications()
    markup = markups.specifications(specifications)
    await message.answer(config.MSG_SPECIFICATION, reply_markup=markup)

    next_state = UserStates.Specification
    await next_state.set()
    await services.user.set_next_state_markup(next_state, keyboard, markup, state)


@dp.message_handler(state=UserStates.Specification)
async def years(
    message: types.Message,
    user: User,
    wrapper: WrapperForBot,
    keyboard: dict,
    state: FSMContext,
):
    specification = message.text
    await services.base.set_data_to_db(user, specification=specification)

    years = await wrapper.years()
    next_state = UserStates.Year
    if len(years) >= 2:
        markup = markups.years(years)
        await message.answer(config.MSG_YEAR, reply_markup=markup)
        await next_state.set()
        await services.user.set_next_state_markup(next_state, keyboard, markup, state)
    else:
        keyboard[next_state.state] = None
        message.text = None
        await main_topic(message, user, wrapper, keyboard, state)


@dp.message_handler(state=UserStates.Year)
async def main_topic(
    message: types.Message,
    user: User,
    wrapper: WrapperForBot,
    keyboard: dict,
    state: FSMContext,
):
    year = None
    if message.text and message.text.isdigit():
        year = int(message.text)
    await services.base.set_data_to_db(user, year=year)

    main_topics = await wrapper.main_topics()
    markup = markups.main_topics(main_topics)
    await message.answer(config.MSG_MAIN_TOPIC, reply_markup=markup)

    next_state = UserStates.Main_topic
    await next_state.set()
    await services.user.set_next_state_markup(next_state, keyboard, markup, state)


@dp.message_handler(state=UserStates.Main_topic)
async def sub_topic(
    message: types.Message,
    user: User,
    wrapper: WrapperForBot,
    keyboard: dict,
    state: FSMContext,
):
    main_topic = message.text
    await services.base.set_data_to_db(user, main_topic=main_topic)

    sub_topics = await wrapper.sub_topics()
    next_state = UserStates.Sub_topic
    if sub_topics:
        markup = markups.sub_topics(sub_topics)
        await message.answer(config.MSG_SUB_TOPIC, reply_markup=markup)

        await next_state.set()
        await services.user.set_next_state_markup(next_state, keyboard, markup, state)
    else:
        keyboard[next_state.state] = None
        message.text = None
        await sub_sub_topic(message, user, wrapper, keyboard, state)


@dp.message_handler(state=UserStates.Sub_topic)
async def sub_sub_topic(
    message: types.Message,
    user: User,
    wrapper: WrapperForBot,
    keyboard: dict,
    state: FSMContext,
):
    sub_topic = message.text
    await services.base.set_data_to_db(user, sub_topic=sub_topic)

    sub_sub_topics = await wrapper.sub_sub_topics()
    next_state = UserStates.Sub_sub_topic
    if sub_sub_topics:
        markup = markups.sub_sub_topics(sub_sub_topics)
        await message.answer(config.MSG_SUB_SUB_TOPIC, reply_markup=markup)

        await next_state.set()
        await services.user.set_next_state_markup(next_state, keyboard, markup, state)
    else:
        keyboard[next_state.state] = None
        message.text = None
        await exercise(message, user, wrapper, keyboard, state)


@dp.message_handler(state=UserStates.Sub_sub_topic)
async def exercise(
    message: types.Message,
    user: User,
    wrapper: WrapperForBot,
    keyboard: dict,
    state: FSMContext,
):
    sub_sub_topic = message.text
    await services.base.set_data_to_db(user, sub_sub_topic=sub_sub_topic)

    exercises = await wrapper.exercises()
    markup = markups.exercises(exercises)
    await message.answer(config.MSG_EXERCISE, reply_markup=markup)

    next_state = UserStates.Exercise
    await next_state.set()
    await services.user.set_next_state_markup(next_state, keyboard, markup, state)


@dp.message_handler(state=UserStates.Exercise)
async def solution(
    message: types.Message,
    user: User,
    wrapper: WrapperForBot,
    keyboard: dict,
    state: FSMContext,
):
    exercise = message.text
    await services.base.set_data_to_db(user, exercise=exercise)

    solution = await wrapper.solution()
    solution_id = int(solution[0])
    solution_url = solution[1]

    await services.user.send_solution_and_save_to_db(
        solution_id, solution_url, message, Photo, httpx_worker
    )
