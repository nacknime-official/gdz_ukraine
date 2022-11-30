from aiogram import Dispatcher

from app.middlewares.acl import ACLMiddleware
from app.middlewares.check_input import Checker
from app.middlewares.item_filter import ItemFilterMiddleware
from app.middlewares.throttling import ThrottlingMiddleware
from app.middlewares.wrapper import WrapperMiddleware
from app.services.item_filter import ItemFilterArgs


def setup(dp: Dispatcher):
    dp.middleware.setup(ThrottlingMiddleware(limit=0.7))
    dp.middleware.setup(ACLMiddleware())
    dp.middleware.setup(WrapperMiddleware())
    dp.middleware.setup(Checker())
    dp.middleware.setup(ItemFilterMiddleware(ItemFilterArgs(subjects=["Русский язык"])))
