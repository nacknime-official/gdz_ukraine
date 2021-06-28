from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.mongo import MongoStorage
from aiogram.utils.executor import Executor

from app import config

bot = Bot(config.TELEGRAM_TOKEN)
storage = MongoStorage(host=config.MONGO_HOST, port=config.MONGO_PORT)
dp = Dispatcher(bot, storage=storage)
runner = Executor(dp)


def setup():
    from app.models import db
    from app import middlewares
    from app import filters

    db.setup(runner)
    middlewares.setup(dp)
    filters.setup(dp)

    import app.handlers
