import os

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

POSTGRES_HOST = os.getenv("POSTGRES_HOST", default="localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", default=5432)
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", default="")
POSTGRES_USER = os.getenv("POSTGRES_USER", default="aiogram")
POSTGRES_DB = os.getenv("POSTGRES_DB", default="aiogram")
POSTGRES_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

MSG_START = "Выберите клас"
MSG_SUBJECT = "Выбери предмет"
MSG_AUTHOR = "Выбери автора"
MSG_SPECIFICATION = "Выбери тип"
MSG_YEARS = "Выбери год"
MSG_MAIN_TOPIC = "Выбери главную тему"
MSG_SUB_TOPIC = "Выбери подтему"
MSG_SUB_SUB_TOPIC = "Выбери подподтему"
MSG_EXERCISE = "Выбери задание"

MSG_WRONG_INPUT = "Тыкни на кнопку внизу"
