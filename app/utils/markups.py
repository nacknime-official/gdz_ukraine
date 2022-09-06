import inspect
import sys
import typing

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from app import config
from app.utils.helper import name_func

NAVIGATION_BUTTONS = (config.BTN_GOTO_START, config.BTN_GOTO_BACK)

def _add_navigation_buttons_per_row(markup: ReplyKeyboardMarkup):
    for btn in NAVIGATION_BUTTONS:
        markup.add(btn)


def grades(*args) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
    buttons: typing.List[str] = [str(i) for i in range(1, 11 + 1)]
    markup.add(*buttons)
    return markup


def subjects(subjects: typing.List[str]) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
    _add_navigation_buttons_per_row(markup)
    markup.add(*subjects)
    return markup


def authors(authors: typing.List[str]) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
    _add_navigation_buttons_per_row(markup)
    markup.add(*authors)
    return markup


def specifications(specifications: typing.List[str]) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
    _add_navigation_buttons_per_row(markup)
    markup.add(*specifications)
    return markup


def years(years: typing.List[typing.Union[str, int]]) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
    _add_navigation_buttons_per_row(markup)
    markup.add(*years)
    return markup


def main_topics(main_topics: typing.List[str]) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
    _add_navigation_buttons_per_row(markup)
    markup.add(*main_topics)
    return markup


def sub_topics(sub_topics: typing.List[str]) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
    _add_navigation_buttons_per_row(markup)
    markup.add(*sub_topics)
    return markup


def sub_sub_topics(sub_sub_topics: typing.List[str]) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
    _add_navigation_buttons_per_row(markup)
    markup.add(*sub_sub_topics)
    return markup


def exercises(exercises: typing.List[str]) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
    _add_navigation_buttons_per_row(markup)
    markup.add(*exercises)
    return markup


def confirm_send_all() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(config.BTN_SEND_ALL_YES, callback_data=config.CB_SEND_ALL_YES))
    markup.add(InlineKeyboardButton(config.BTN_SEND_ALL_NO, callback_data=config.CB_SEND_ALL_NO))
    return markup


def confirm_send_notifs() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(config.BTN_SEND_NOTIFS_YES, callback_data=config.CB_SEND_NOTIFS_YES))
    markup.add(InlineKeyboardButton(config.BTN_SEND_NOTIFS_NO, callback_data=config.CB_SEND_NOTIFS_NO))
    return markup


def confirm_block() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(config.BTN_BLOCK_YES, callback_data=config.CB_BLOCK_YES))
    markup.add(InlineKeyboardButton(config.BTN_BLOCK_NO, callback_data=config.CB_BLOCK_NO))
    return markup


def confirm_unblock() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(config.BTN_UNBLOCK_YES, callback_data=config.CB_UNBLOCK_YES))
    markup.add(InlineKeyboardButton(config.BTN_UNBLOCK_NO, callback_data=config.CB_UNBLOCK_NO))
    return markup


markups_list: typing.List[name_func] = [
    name_func(name, func)
    for name, func in inspect.getmembers(sys.modules[__name__], inspect.isfunction)
]
