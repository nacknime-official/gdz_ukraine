import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
ADMIN_USERNAME = str(os.getenv("ADMIN_USERNAME"))

POSTGRES_HOST = os.getenv("POSTGRES_HOST", default="localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", default=5432)
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", default="")
POSTGRES_USER = os.getenv("POSTGRES_USER", default="aiogram")
POSTGRES_DB = os.getenv("POSTGRES_DB", default="aiogram")
POSTGRES_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

MONGO_HOST = os.getenv("MONGO_HOST", default="localhost")
MONGO_PORT = os.getenv("MONGO_PORT", default="27017")

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", default="localhost")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", default=5672))
RABBITMQ_USER = os.getenv("RABBITMQ_USER", default="guest")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", default="guest")
RABBITMQ_EXCHANGE_NAME = os.getenv("RABBITMQ_EXCHANGE_NAME", default="broadcast")
RABBITMQ_QUEUE_NAME = os.getenv("RABBITMQ_QUEUE_NAME", default="broadcast")

PREFIX_WRONG_PHOTO_SIZE = "wrong_size_"
WATERMARK_PATH = str(Path.cwd() / "static" / "watermark.png")

# user messages
MSG_START = "Вибери клас"
MSG_SUBJECT = "Вибери предмет"
MSG_AUTHOR = "Вибери автора"
MSG_SPECIFICATION = "Вибери тип"
MSG_YEAR = "Вибери рік"
MSG_MAIN_TOPIC = "Вибери головну тему"
MSG_SUB_TOPIC = "Вибери підтему"
MSG_SUB_SUB_TOPIC = "Вибери підпідтему"
MSG_EXERCISE = "Вибери завдання"
MSG_WRONG_INPUT = "Тицьни на кнопку знизу"
MSG_COMMAND_NOT_FOUND = "Такої команди немає"
MSG_SOMETHING_GOES_WRONG_GO_START = "Щось пішло не так... Тицьни на /start"

# user buttons
BTN_GOTO_START = "Головне меню"
BTN_GOTO_BACK = "Назад"

# admin messages
MSG_INPUT_SEND_ALL = "Введіть текст для розсилки"
MSG_SUCCESSFUL_SEND_ALL = "Успішно відправлено {} юзерам"
MSG_INPUT_SEND_NOTIFS = "Введіть текст для розсилки"
MSG_SUCCESSFUL_SEND_NOTIFS = "Успішно відправлено {} юзерам"
MSG_BEGIN_COUNTING_ALIVE_USERS = "Підрахунок юзерів почався"
MSG_END_COUNTING_ALIVE_USERS = "Підрахунок закінчений! Всього {} юзерів"
MSG_DONT_WANNA = "Ну як хочете :)"
MSG_SEND_OR_NOT = "Відправити?"
MSG_INPUT_BLOCKING_USER_ID = "Введіть айді юзера, якого треба заблокувати"
MSG_WRONG_BLOCKING_USER_ID = "Це не айдішник юзера, спробуй ще раз, але з числами"
MSG_THIS_USER = "Цей"
MSG_USER_ALREADY_BLOCKED_DO_YOU_WANNA_UNBLOCK = (
    "юзер вже заблокований. Бажаєте його розблокувати?"
)
MSG_BLOCK_SURE = "Ви впевнені, що хочете заблокувати цього юзера?"
MSG_SUCCESSFUL_BLOCK = "Ви успішно заблокували цього юзера"
MSG_SUCCESSFUL_UNBLOCK = "Ви успішно розблокували цього юзера"
MSG_WRONG_TOGGLE_NOTIFS_USER_ID = "Це не айдішник юзера, спробуй ще раз, але з числами"

# admin buttons
BTN_SEND_ALL_YES = "Так"
BTN_SEND_ALL_NO = "Ні"
BTN_SEND_NOTIFS_YES = "Так"
BTN_SEND_NOTIFS_NO = "Ні"
BTN_BLOCK_YES = "Так"
BTN_BLOCK_NO = "Ні"
BTN_UNBLOCK_YES = "Так"
BTN_UNBLOCK_NO = "Ні"

# admin callback data
CB_SEND_ALL_YES = "send_all_yes"
CB_SEND_ALL_NO = "send_all_no"
CB_SEND_NOTIFS_YES = "send_notifs_yes"
CB_SEND_NOTIFS_NO = "send_notifs_no"
CB_BLOCK_YES = "block_yes"
CB_BLOCK_NO = "block_no"
CB_UNBLOCK_YES = "unblock_yes"
CB_UNBLOCK_NO = "unblock_no"
