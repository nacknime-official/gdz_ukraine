from io import BytesIO

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import PhotoDimensions

from app import config
from app.misc import dp
from app.models.photo import Photo
from app.models.user import User
from app.utils import markups
from app.utils.httpx import httpx_worker
from app.utils.states import UserStates, quiz, state_messages
from app.utils.wrapper_vshkole import WrapperFotBot


@dp.message_handler(text="Назад", state=quiz)
async def back(message: types.Message, user: User, keyboard: dict, state: FSMContext):
    msg = None
    while not msg:
        prev_state = await UserStates.previous()
        markup = keyboard.get(prev_state)
        if markup is None:
            continue
        else:
            msg = state_messages[prev_state]

    await message.answer(msg, reply_markup=markup)


@dp.message_handler(text="Главное меню", state="*")
@dp.message_handler(commands="start", state="*")
async def cmd_start(message: types.Message, user: User, state: FSMContext):
    markup = markups.classes()
    await message.answer(config.MSG_START, reply_markup=markup)
    await UserStates.Grade.set()
    await state.update_data(Keyboard={UserStates.Grade.state: markup.to_python()})


@dp.message_handler(lambda message: message.is_command(), state="*")
async def cmd_any(message: types.Message, user: User, state: FSMContext):
    await message.answer("Такой команды нету")


@dp.message_handler(state=UserStates.Grade)
async def subject(
        message: types.Message,
        user: User,
        wrapper: WrapperFotBot,
        keyboard: dict,
        state: FSMContext,
):
    grade = int(message.text)
    await user.update(grade=grade).apply()

    subjects = await wrapper.subjects()
    subjects_name = [subject["name"] for subject in subjects]
    markup = markups.subjects(subjects_name)
    await message.answer(config.MSG_SUBJECT, reply_markup=markup)

    next_state = UserStates.Subject
    await next_state.set()
    keyboard[next_state.state] = markup.to_python()
    await state.update_data(Keyboard=keyboard, Wrapper_subjects=subjects)


@dp.message_handler(state=UserStates.Subject)
async def author(
        message: types.Message,
        user: User,
        wrapper: WrapperFotBot,
        keyboard: dict,
        state: FSMContext,
):
    subject = message.text
    await user.update(subject=subject).apply()

    authors, entities = await wrapper.authors()
    markup = markups.authors(authors)
    await message.answer(config.MSG_AUTHOR, reply_markup=markup)

    next_state = UserStates.Author
    await next_state.set()
    keyboard[next_state.state] = markup.to_python()
    await state.update_data(Keyboard=keyboard, Wrapper_subject_entities=entities)


@dp.message_handler(state=UserStates.Author)
async def specifications(
        message: types.Message,
        user: User,
        wrapper: WrapperFotBot,
        keyboard: dict,
        state: FSMContext,
):
    author = message.text
    await user.update(author=author).apply()

    specifications = await wrapper.specifications()
    markup = markups.specifications(specifications)
    await message.answer(config.MSG_SPECIFICATION, reply_markup=markup)

    next_state = UserStates.Specification
    await next_state.set()
    keyboard[next_state.state] = markup.to_python()
    await state.update_data(Keyboard=keyboard)


@dp.message_handler(state=UserStates.Specification)
async def years(
        message: types.Message,
        user: User,
        wrapper: WrapperFotBot,
        keyboard: dict,
        state: FSMContext,
):
    specification = message.text
    await user.update(specification=specification).apply()

    years = await wrapper.years()
    next_state = UserStates.Years
    if len(years) >= 2:
        markup = markups.years(years)
        await message.answer(config.MSG_YEARS, reply_markup=markup)
        await next_state.set()
        keyboard[next_state.state] = markup.to_python()
        await state.update_data(Keyboard=keyboard)
    else:
        keyboard[next_state.state] = None
        message.text = None
        await main_topic(message, user, wrapper, keyboard, state)


@dp.message_handler(state=UserStates.Years)
async def main_topic(
        message: types.Message,
        user: User,
        wrapper: WrapperFotBot,
        keyboard: dict,
        state: FSMContext,
):
    if message.text and message.text.isdigit():
        year = int(message.text)
        await user.update(year=year).apply()
    else:
        await user.update(year=None).apply()

    main_topics, entities = await wrapper.main_topics()
    markup = markups.main_topics(main_topics)
    await message.answer(config.MSG_MAIN_TOPIC, reply_markup=markup)

    next_state = UserStates.Main_topic
    await next_state.set()
    keyboard[next_state.state] = markup.to_python()
    await state.update_data(Keyboard=keyboard, Wrapper_entities=entities)


@dp.message_handler(state=UserStates.Main_topic)
async def sub_topic(
        message: types.Message,
        user: User,
        wrapper: WrapperFotBot,
        keyboard: dict,
        state: FSMContext,
):
    main_topic = message.text
    await user.update(main_topic=main_topic).apply()

    sub_topics = await wrapper.sub_topics()
    next_state = UserStates.Sub_topic
    if sub_topics:
        markup = markups.sub_topics(sub_topics)
        await message.answer(config.MSG_SUB_TOPIC, reply_markup=markup)

        await next_state.set()
        keyboard[next_state.state] = markup.to_python()
        await state.update_data(Keyboard=keyboard)
    else:
        keyboard[next_state.state] = None
        message.text = None
        await sub_sub_topic(message, user, wrapper, keyboard, state)


@dp.message_handler(state=UserStates.Sub_topic)
async def sub_sub_topic(
        message: types.Message,
        user: User,
        wrapper: WrapperFotBot,
        keyboard: dict,
        state: FSMContext,
):
    sub_topic = message.text
    await user.update(sub_topic=sub_topic).apply()

    sub_sub_topics = await wrapper.sub_sub_topics()
    next_state = UserStates.Sub_sub_topic
    if sub_sub_topics:
        markup = markups.sub_sub_topics(sub_sub_topics)
        await message.answer(config.MSG_SUB_SUB_TOPIC, reply_markup=markup)

        await next_state.set()
        keyboard[next_state.state] = markup.to_python()
        await state.update_data(Keyboard=keyboard)
    else:
        keyboard[next_state.state] = None
        message.text = None
        await exercise(message, user, wrapper, keyboard, state)


@dp.message_handler(state=UserStates.Sub_sub_topic)
async def exercise(
        message: types.Message,
        user: User,
        wrapper: WrapperFotBot,
        keyboard: dict,
        state: FSMContext,
):
    sub_sub_topic = message.text
    if sub_sub_topic:
        await user.update(sub_sub_topic=sub_sub_topic).apply()
    else:
        await user.update(sub_sub_topic=None).apply()

    exercises = await wrapper.exercises()
    markup = markups.exercises(exercises)
    await message.answer(config.MSG_EXERCISE, reply_markup=markup)

    next_state = UserStates.Exercise
    await next_state.set()
    keyboard[next_state.state] = markup.to_python()
    await state.update_data(Keyboard=keyboard)


@dp.message_handler(state=UserStates.Exercise)
async def solution(
        message: types.Message,
        user: User,
        wrapper: WrapperFotBot,
        keyboard: dict,
        state: FSMContext,
):
    exercise = message.text
    await user.update(exercise=exercise).apply()

    solution = await wrapper.solution()
    solution_id = int(solution[0])
    solution_url = solution[1]
    photo = await Photo.get(solution_id)

    if not photo:
        img = await httpx_worker.get(solution_url)
        img_content = img.content
        img_filename = img.url.path.split("/")[-1]

        try:
            img_id = (await message.answer_photo(img_content)).photo[-1].file_id
        except PhotoDimensions as e:
            img_id = (
                await message.answer_document(
                    types.InputFile(BytesIO(img_content), filename=img_filename)
                )
            ).document.file_id
            img_id = config.PREFIX_WRONG_PHOTO_SIZE + img_id

        photo = await Photo.create(id=solution_id, photo_id=img_id)
    else:
        img_id = photo.photo_id
        if img_id.startswith(config.PREFIX_WRONG_PHOTO_SIZE):
            await message.answer_document(img_id[len(config.PREFIX_WRONG_PHOTO_SIZE) :])
        else:
            await message.answer_photo(img_id)
