from aiogram import Dispatcher


def setup(dp: Dispatcher):
    from .admin import IsAdmin

    dp.filters_factory.bind(IsAdmin)
