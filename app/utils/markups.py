import typing

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from app import config


def classes() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
    buttons: typing.List[str] = [str(i) for i in range(1, 11 + 1)]
    markup.add(*buttons)
    return markup


def subjects(subjects: typing.List[str]) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
    markup.add("Главное меню")
    markup.add("Назад")
    markup.add(*subjects)
    return markup


def authors(authors: typing.List[str]) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
    markup.add("Главное меню")
    markup.add("Назад")
    markup.add(*authors)
    return markup


def specifications(specifications: typing.List[str]) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
    markup.add("Главное меню")
    markup.add("Назад")
    markup.add(*specifications)
    return markup


def years(years: typing.List[typing.Union[str, int]]) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
    markup.add("Главное меню")
    markup.add("Назад")
    markup.add(*years)
    return markup


def main_topics(main_topics: typing.List[str]) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
    markup.add("Главное меню")
    markup.add("Назад")
    markup.add(*main_topics)
    return markup


def sub_topics(sub_topics: typing.List[str]) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
    markup.add("Главное меню")
    markup.add("Назад")
    markup.add(*sub_topics)
    return markup


def sub_sub_topics(sub_sub_topics: typing.List[str]) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
    markup.add("Главное меню")
    markup.add("Назад")
    markup.add(*sub_sub_topics)
    return markup


def exercises(exercises: typing.List[str]) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
    markup.add("Главное меню")
    markup.add("Назад")
    markup.add(*exercises)
    return markup


def confirm_send_all() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Да", callback_data=config.CB_SEND_ALL_YES))
    markup.add(InlineKeyboardButton("Нет", callback_data=config.CB_SEND_ALL_NO))
    return markup


def confirm_block() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Да", callback_data=config.CB_BLOCK_YES))
    markup.add(InlineKeyboardButton("Нет", callback_data=config.CB_BLOCK_NO))
    return markup


def confirm_unblock() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Да", callback_data=config.CB_UNBLOCK_YES))
    markup.add(InlineKeyboardButton("Нет", callback_data=config.CB_UNBLOCK_NO))
    return markup
