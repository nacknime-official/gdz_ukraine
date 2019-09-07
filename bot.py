from aiogram import Bot, Dispatcher, executor
import requests
from config import TOKEN
import dbworker as db
import markups
import pickle

# initialize bot
bot = Bot(TOKEN)
dp = Dispatcher(bot)


# func for button "back"
@dp.message_handler(lambda message: message.text == "Назад")
async def back(message):
    data = pickle.loads(db.get_keyboard_and_msg(message.chat.id))
    subtopic = db.get_subtopic(message.chat.id)
    subsubtopic = db.get_subsubtopic(message.chat.id)
    state = db.get_current_state(message.chat.id)
    if state == 8 and subtopic == 'None':
        db.set_state(str(state - 3), message.chat.id)
        markup, msg = data[str(state - 3)]
    elif state == 8 and subsubtopic == 'None':
        db.set_state(str(state - 2), message.chat.id)
        markup, msg = data[str(state - 2)]
    elif state <= 1:
        db.set_state("1", message.chat.id)
        markup = markups.klas()
        msg = "Выбери клас"
    else:
        db.set_state(str(state - 1), message.chat.id)
        markup, msg = data[str(state - 1)]
    await bot.send_message(message.chat.id, msg, reply_markup=markup)


# help
@dp.message_handler(commands='help')
async def help(message):
    await bot.send_message(message.chat.id, """
Open Source бот, который покажет тебе решение для твоей домашки максимально быстро!
GitHub: https://github.com/Maks4816/gdz_ukraine
Приму все пожелания и идеи для доработки бота - @nacknime
        """)


# send some message to all users
@dp.message_handler(commands='send_all')
async def send_all(message):
    if message.chat.id == 399925974:
        text = message.text[10:]
        for user in db.get_all_users():
            print(user)
            try:
                await bot.send_message(user,
                                       text)
            except Exception as e:
                print(e)


# /start - choice the grade
@dp.message_handler(lambda message: message.text == "Главное меню")
@dp.message_handler(commands=['start'])
async def start(message):
    db.get_and_set_id(message.chat.id)
    markup = markups.klas()
    msg = await bot.send_message(message.chat.id, "Выбери клас", reply_markup=markup)
    db.set_state('1', message.chat.id)                                          # set state to '1' for specific ID
    data = pickle.dumps({'1': [markup, msg.text]})                              # convert to bytes for save in DB
    db.set_keyboard_and_msg(data, message.chat.id)                              # save keyboard and msg in DB for 'back' function


# choice subject
@dp.message_handler(lambda message: db.get_current_state(message.chat.id) == 1)
async def subject(message):
    # check a message on correct input
    data = pickle.loads(db.get_keyboard_and_msg(message.chat.id))            # get keyboard and msg from DB, convert back to dict with objects
    markup = data[str(db.get_current_state(message.chat.id))][0]             # get only markup from list
    if message.text not in [j['text'] for i in markup.keyboard for j in i]:  # if message.text not in buttons text
        await bot.send_message(message.chat.id, "Нажми на кнопку!")
        return                                                               # next code will not be executed, return to start of this handler
    klas = message.text.split()[0]                                           # '5 клас' -> split -> ['5', 'клас'] -> get 1st element -> '5'
    db.set_klas(klas, message.chat.id)
    markup = markups.subject(klas)
    msg = await bot.send_message(message.chat.id, "Выбери предмет", reply_markup=markup)
    db.set_state('2', message.chat.id)
    data['2'] = [markup, msg.text]                                           # keyboard and msg added to dict with key '2' (step 2)
    db.set_keyboard_and_msg(pickle.dumps(data), message.chat.id)             # convert to bytes with pickle and set it to DB


# choice author
@dp.message_handler(lambda message: db.get_current_state(message.chat.id) == 2)
async def author(message):
    data = pickle.loads(db.get_keyboard_and_msg(message.chat.id))
    markup = data[str(db.get_current_state(message.chat.id))][0]
    if message.text not in [j['text'] for i in markup.keyboard for j in i]:
        await bot.send_message(message.chat.id, "Нажми на кнопку!")
        return
    subject = message.text
    db.set_subject(subject, message.chat.id)                                  # set subject to DB
    klas = db.get_klas(message.chat.id)                                       # get grade for markup
    markup = markups.author(klas, subject)
    msg = await bot.send_message(message.chat.id, "Выбери автора", reply_markup=markup)
    db.set_state('3', message.chat.id)
    data['3'] = [markup, msg.text]
    db.set_keyboard_and_msg(pickle.dumps(data), message.chat.id)


# choice type
@dp.message_handler(lambda message: db.get_current_state(message.chat.id) == 3)
async def type(message):
    data = pickle.loads(db.get_keyboard_and_msg(message.chat.id))
    markup = data[str(db.get_current_state(message.chat.id))][0]
    if message.text not in [j['text'] for i in markup.keyboard for j in i]:
        await bot.send_message(message.chat.id, "Нажми на кнопку!")
        return
    author = message.text
    db.set_author(author, message.chat.id)
    klas = db.get_klas(message.chat.id)
    subject = db.get_subject(message.chat.id)
    markup = markups.type(klas, subject, author)
    msg = await bot.send_message(message.chat.id, "Выбери тип", reply_markup=markup)
    db.set_state('4', message.chat.id)
    data['4'] = [markup, msg.text]
    db.set_keyboard_and_msg(pickle.dumps(data), message.chat.id)


# choice maintopic
@dp.message_handler(lambda message: db.get_current_state(message.chat.id) == 4)
async def maintopic(message):
    data = pickle.loads(db.get_keyboard_and_msg(message.chat.id))
    markup = data[str(db.get_current_state(message.chat.id))][0]
    if message.text not in [j['text'] for i in markup.keyboard for j in i]:
        await bot.send_message(message.chat.id, "Нажми на кнопку!")
        return
    type = message.text
    db.set_type(type, message.chat.id)
    klas = db.get_klas(message.chat.id)
    subject = db.get_subject(message.chat.id)
    author = db.get_author(message.chat.id)
    markup = markups.maintopic(klas, subject, author, type)
    msg = await bot.send_message(message.chat.id, "Выбери главную тему", reply_markup=markup)
    db.set_state('5', message.chat.id)
    data['5'] = [markup, msg.text]
    db.set_keyboard_and_msg(pickle.dumps(data), message.chat.id)


# choice subtopic
@dp.message_handler(lambda message: db.get_current_state(message.chat.id) == 5)
async def subtopic(message):
    data = pickle.loads(db.get_keyboard_and_msg(message.chat.id))
    markup = data[str(db.get_current_state(message.chat.id))][0]
    if message.text not in [j['text'] for i in markup.keyboard for j in i]:
        await bot.send_message(message.chat.id, "Нажми на кнопку!")
        return
    maintopic = message.text
    db.set_maintopic(maintopic, message.chat.id)
    klas = db.get_klas(message.chat.id)
    subject = db.get_subject(message.chat.id)
    author = db.get_author(message.chat.id)
    type = db.get_type(message.chat.id)
    markup = markups.subtopic(klas, subject, author, type, maintopic)
    if markup.keyboard[2][0]['text'] != 'None':                                         # if 1st button's text != 'None': continue
        msg = await bot.send_message(message.chat.id, "Выбери подтему", reply_markup=markup)  # 'subtopic' may not be, so we do a check
        db.set_state('6', message.chat.id)
        data['6'] = [markup, msg.text]
        db.set_keyboard_and_msg(pickle.dumps(data), message.chat.id)
    else:                                                                               # else we set next params to 'None' and...
        db.set_subtopic('None', message.chat.id)                                        # ... jump to choice exercise
        db.set_subsubtopic('None', message.chat.id)
        markup = markups.exercise(klas, subject, author, type, maintopic, subtopic='None', subsubtopic='None')
        msg = await bot.send_message(message.chat.id, "Выбери задание", reply_markup=markup)
        db.set_state('8', message.chat.id)
        data['8'] = [markup, msg.text]
        db.set_keyboard_and_msg(pickle.dumps(data), message.chat.id)


# choice subsubtopic :)
@dp.message_handler(lambda message: db.get_current_state(message.chat.id) == 6)
async def subsubtopic(message):
    data = pickle.loads(db.get_keyboard_and_msg(message.chat.id))
    markup = data[str(db.get_current_state(message.chat.id))][0]
    if message.text not in [j['text'] for i in markup.keyboard for j in i]:
        await bot.send_message(message.chat.id, "Нажми на кнопку!")
        return
    subtopic = message.text
    db.set_subtopic(subtopic, message.chat.id)
    klas = db.get_klas(message.chat.id)
    subject = db.get_subject(message.chat.id)
    author = db.get_author(message.chat.id)
    type = db.get_type(message.chat.id)
    maintopic = db.get_maintopic(message.chat.id)
    markup = markups.subsubtopic(klas, subject, author, type, maintopic, subtopic)
    if markup.keyboard[2][0]['text'] != 'None':
        msg = await bot.send_message(message.chat.id, "Выбери подподтему", reply_markup=markup)
        db.set_state('7', message.chat.id)
        data['7'] = [markup, msg.text]
        db.set_keyboard_and_msg(pickle.dumps(data), message.chat.id)
    else:
        db.set_subsubtopic('None', message.chat.id)
        markup = markups.exercise(klas, subject, author, type, maintopic, subtopic, subsubtopic='None')
        msg = await bot.send_message(message.chat.id, "Выбери задание", reply_markup=markup)
        db.set_state('8', message.chat.id)
        data['8'] = [markup, msg.text]
        db.set_keyboard_and_msg(pickle.dumps(data), message.chat.id)


# choice exercise
@dp.message_handler(lambda message: db.get_current_state(message.chat.id) == 7)
async def exercise(message):
    data = pickle.loads(db.get_keyboard_and_msg(message.chat.id))
    markup = data[str(db.get_current_state(message.chat.id))][0]
    if message.text not in [j['text'] for i in markup.keyboard for j in i]:
        await bot.send_message(message.chat.id, "Нажми на кнопку!")
        return
    subsubtopic = message.text
    db.set_subsubtopic(subsubtopic, message.chat.id)
    klas = db.get_klas(message.chat.id)
    subject = db.get_subject(message.chat.id)
    author = db.get_author(message.chat.id)
    type = db.get_type(message.chat.id)
    maintopic = db.get_maintopic(message.chat.id)
    subtopic = db.get_subtopic(message.chat.id)
    subsubtopic = db.get_subsubtopic(message.chat.id)
    markup = markups.exercise(klas, subject, author, type, maintopic, subtopic, subsubtopic)
    msg = await bot.send_message(message.chat.id, "Выбери задание", reply_markup=markup)
    db.set_state('8', message.chat.id)
    data['8'] = [markup, msg.text]
    db.set_keyboard_and_msg(pickle.dumps(data), message.chat.id)


# get solution
@dp.message_handler(lambda message: db.get_current_state(message.chat.id) == 8)
async def solution(message):
    data = pickle.loads(db.get_keyboard_and_msg(message.chat.id))
    markup = data[str(db.get_current_state(message.chat.id))][0]
    if message.text not in [j['text'] for i in markup.keyboard for j in i]:
        await bot.send_message(message.chat.id, "Нажми на кнопку!")
        return
    exercise = message.text
    db.set_exercise(exercise, message.chat.id)
    klas = db.get_klas(message.chat.id)
    subject = db.get_subject(message.chat.id)
    author = db.get_author(message.chat.id)
    type = db.get_type(message.chat.id)
    maintopic = db.get_maintopic(message.chat.id)
    subtopic = db.get_subtopic(message.chat.id)
    subsubtopic = db.get_subsubtopic(message.chat.id)
    solution = db.get_solution(klas, subject, author, type, maintopic, subtopic, subsubtopic, exercise)  # may return link on photo or file_id if exists
    if solution.startswith('/'):                                                                         # link starts with '/'
        r = requests.get('https://cdn.gdz4you.com' + solution).content
        try:
            img = (await bot.send_photo(message.chat.id, r)).photo[-1].file_id                                  # get photo id after send that
        except Exception as e:
            print(e)
            img = (await bot.send_document(message.chat.id, 'https://cdn.gdz4you.com' + solution)).document.file_id
            img = "big_" + img
        db.set_solution(klas, subject, author, type, maintopic, subtopic, subsubtopic, exercise, img)    # set file_id to 'gdz'
    elif solution.startswith("big_"):
        await bot.send_document(message.chat.id, solution[4:])                                           # if get a file id: send it by file id
    else:
        await bot.send_photo(message.chat.id, solution)


executor.start_polling(dp)
