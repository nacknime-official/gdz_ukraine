from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.utils.executor import Executor

from app import config

bot = Bot(config.TELEGRAM_TOKEN)
storage = RedisStorage2()
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
