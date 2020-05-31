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

ADMIN_ID = int(os.getenv("ADMIN_ID"))

# user messages
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

# admin messages
MSG_INPUT_SEND_ALL = "Введите текст для рассылки"
MSG_SUCCESFUL_SEND_ALL = "Успешно отправлено {} юзерам"
MSG_DONT_WANNA_SEND_ALL = "Ну как хотите :)"

# admin callback data
CB_SEND_ALL_YES = "send_all_yes"
CB_SEND_ALL_NO = "send_all_no"

ADMIN_COMMANDS = ["/send_all"]
