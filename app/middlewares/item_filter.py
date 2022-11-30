from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from app.services.item_filter import (
    AuthorsFilter,
    ExercisesFilter,
    ItemFilterArgs,
    ItemFilters,
    MainTopicsFilter,
    SpecificationsFilter,
    SubjectsFilter,
    SubSubTopicsFilter,
    SubTopicsFilter,
    YearsFilter,
)


class ItemFilterMiddleware(BaseMiddleware):
    def __init__(self, args: ItemFilterArgs):
        self.item_filters = ItemFilters(
            SubjectsFilter(args.subjects),
            AuthorsFilter(args.authors),
            SpecificationsFilter(args.specifications),
            YearsFilter(args.years),
            MainTopicsFilter(args.main_topics),
            SubTopicsFilter(args.sub_topics),
            SubSubTopicsFilter(args.sub_sub_topics),
            ExercisesFilter(args.exercises),
        )
        super(ItemFilterMiddleware, self).__init__()

    async def on_process_message(self, _: types.Message, data: dict):
        data["item_filters"] = self.item_filters
