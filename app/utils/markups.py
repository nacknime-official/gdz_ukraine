from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from app import config


def classes():
    markup = ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
    buttons = [str(i) for i in range(1, 11 + 1)]
    markup.add(*buttons)
    return markup


def subjects(subjects):
    markup = ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
    markup.add("Главное меню")
    markup.add("Назад")
    markup.add(*subjects)
    return markup


def authors(authors):
    markup = ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
    markup.add("Главное меню")
    markup.add("Назад")
    markup.add(*authors)
    return markup


def specifications(specifications):
    markup = ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
    markup.add("Главное меню")
    markup.add("Назад")
    markup.add(*specifications)
    return markup


def years(years):
    markup = ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
    markup.add("Главное меню")
    markup.add("Назад")
    markup.add(*years)
    return markup


def main_topics(main_topics):
    markup = ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
    markup.add("Главное меню")
    markup.add("Назад")
    markup.add(*main_topics)
    return markup


def sub_topics(sub_topics):
    markup = ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
    markup.add("Главное меню")
    markup.add("Назад")
    markup.add(*sub_topics)
    return markup


def sub_sub_topics(sub_sub_topics):
    markup = ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
    markup.add("Главное меню")
    markup.add("Назад")
    markup.add(*sub_sub_topics)
    return markup


def exercises(exercises):
    markup = ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
    markup.add("Главное меню")
    markup.add("Назад")
    markup.add(*exercises)
    return markup


def confirm_send_all():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Да", callback_data=config.CB_SEND_ALL_YES))
    markup.add(InlineKeyboardButton("Нет", callback_data=config.CB_SEND_ALL_NO))
    return markup


def confirm_block():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Да", callback_data=config.CB_BLOCK_YES))
    markup.add(InlineKeyboardButton("Нет", callback_data=config.CB_BLOCK_NO))
    return markup


def confirm_unblock():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Да", callback_data=config.CB_UNBLOCK_YES))
    markup.add(InlineKeyboardButton("Нет", callback_data=config.CB_UNBLOCK_NO))
    return markup
