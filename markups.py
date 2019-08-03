from telebot import types
import dbworker as db


def klas():
    markup = types.ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
    buttons = [types.KeyboardButton(i) for i in [f"{i} клас" for i in range(5, 12)]]
    markup.add(*buttons)
    return markup


def subject(klas):
    markup = types.ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
    buttons = [types.KeyboardButton(i) for i in [j for i in db.get_subjects(klas) for j in i]]
    markup.add(types.KeyboardButton("Назад"))
    markup.add(*buttons)
    return markup

def author(klas, subject):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = [types.KeyboardButton(i) for i in [j for i in db.get_authors(klas, subject) for j in i]]
    markup.add(types.KeyboardButton("Назад"))
    markup.add(*buttons)
    return markup

def type(klas, subject, author):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    buttons = [types.KeyboardButton(i) for i in [j for i in db.get_types(klas, subject, author) for j in i]]
    markup.add(types.KeyboardButton("Назад"))
    markup.add(*buttons)
    return markup

def maintopic(klas, subject, author, type):
    markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    buttons = [types.KeyboardButton(i) for i in [j for i in db.get_maintopics(klas, subject, author, type) for j in i]]
    markup.add(types.KeyboardButton("Назад"))
    markup.add(*buttons)
    return markup

def subtopic(klas, subject, author, type, maintopic):
    markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    buttons = [types.KeyboardButton(i) for i in [j for i in db.get_subtopics(klas, subject, author, type, maintopic) for j in i]]
    markup.add(types.KeyboardButton("Назад"))
    markup.add(*buttons)
    return markup

def subsubtopic(klas, subject, author, type, maintopic, subtopic):
    markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    buttons = [types.KeyboardButton(i) for i in [j for i in db.get_subsubtopics(klas, subject, author, type, maintopic, subtopic) for j in i]]
    markup.add(types.KeyboardButton("Назад"))
    markup.add(*buttons)
    return markup

def exercise(klas, subject, author, type, maintopic, subtopic, subsubtopic):
    markup = types.ReplyKeyboardMarkup(row_width=7, resize_keyboard=True)
    buttons = [types.KeyboardButton(i) for i in [j for i in db.get_exercises(klas, subject, author, type, maintopic, subtopic, subsubtopic) for j in i]]
    print(buttons)
    markup.add(types.KeyboardButton("Назад"))
    markup.add(*buttons)
    return markup
