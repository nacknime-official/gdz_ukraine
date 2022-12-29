from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, List, Optional, TypeVar

T = TypeVar("T")

# interface


class ItemFilter(ABC, Generic[T]):
    @abstractmethod
    async def filter(self, input: List[T]) -> List[T]:
        pass


# impl


class _AbstractItemFilter(ItemFilter, Generic[T]):
    def __init__(self, filter_items: Optional[List[T]]):
        self.filter_items = filter_items

    @staticmethod
    def _filter(filtering_items: List[T], filter_items: Optional[List[T]]) -> List[T]:
        if filter_items is None:
            return filtering_items
        return [i for i in filtering_items if i not in filter_items]

    async def filter(self, input: List[T]) -> List[T]:
        return self._filter(input, self.filter_items)


class SubjectsFilter(_AbstractItemFilter):
    ...


class AuthorsFilter(_AbstractItemFilter):
    ...


class SpecificationsFilter(_AbstractItemFilter):
    ...


class YearsFilter(_AbstractItemFilter):
    ...


class MainTopicsFilter(_AbstractItemFilter):
    ...


class SubTopicsFilter(_AbstractItemFilter):
    ...


class SubSubTopicsFilter(_AbstractItemFilter):
    ...


class ExercisesFilter(_AbstractItemFilter):
    ...


# others


@dataclass
class ItemFilterArgs:
    subjects: Optional[List[str]] = None
    authors: Optional[List[str]] = None
    specifications: Optional[List[str]] = None
    years: Optional[List[int]] = None
    main_topics: Optional[List[str]] = None
    sub_topics: Optional[List[str]] = None
    sub_sub_topics: Optional[List[str]] = None
    exercises: Optional[List[str]] = None


@dataclass
class ItemFilters:
    subjects: ItemFilter[str]
    authors: ItemFilter[str]
    specifications: ItemFilter[str]
    years: ItemFilter[int]
    main_topics: ItemFilter[str]
    sub_topics: ItemFilter[str]
    sub_sub_topics: ItemFilter[str]
    exercises: ItemFilter[str]
