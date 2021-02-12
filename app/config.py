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

REDIS_HOST = os.getenv("REDIS_HOST", default="localhost")
REDIS_PORT = os.getenv("REDIS_PORT", default="6379")
REDIS_DB_FSM = os.getenv("REDIS_DB_FSM", default=0)

PREFIX_WRONG_PHOTO_SIZE = "wrong_size_"
WATERMARK_PATH = str(Path.cwd() / "static" / "watermark.png")

# user messages
MSG_START = "Выберите клас"
MSG_SUBJECT = "Выбери предмет"
MSG_AUTHOR = "Выбери автора"
MSG_SPECIFICATION = "Выбери тип"
MSG_YEAR = "Выбери год"
MSG_MAIN_TOPIC = "Выбери главную тему"
MSG_SUB_TOPIC = "Выбери подтему"
MSG_SUB_SUB_TOPIC = "Выбери подподтему"
MSG_EXERCISE = "Выбери задание"
MSG_WRONG_INPUT = "Тыкни на кнопку внизу"

# admin messages
MSG_INPUT_SEND_ALL = "Введите текст для рассылки"
MSG_SUCCESFUL_SEND_ALL = "Успешно отправлено {} юзерам"
MSG_DONT_WANNA = "Ну как хотите :)"

# admin callback data
CB_SEND_ALL_YES = "send_all_yes"
CB_SEND_ALL_NO = "send_all_no"
CB_BLOCK_YES = "block_yes"
CB_BLOCK_NO = "block_no"
CB_UNBLOCK_YES = "unblock_yes"
CB_UNBLOCK_NO = "unblock_no"
