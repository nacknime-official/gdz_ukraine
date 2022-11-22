from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional


class ItemFiltererI(ABC):
    @abstractmethod
    async def subjects_filter(self, input: List[str]) -> List[str]:
        pass

    @abstractmethod
    async def authors_filter(self, input: List[str]) -> List[str]:
        pass

    @abstractmethod
    async def specifications_filter(self, input: List[str]) -> List[str]:
        pass

    @abstractmethod
    async def years_filter(self, input: List[int]) -> List[int]:
        pass

    @abstractmethod
    async def main_topics_filter(self, input: List[str]) -> List[str]:
        pass

    @abstractmethod
    async def sub_topics_filter(self, input: List[str]) -> List[str]:
        pass

    @abstractmethod
    async def sub_sub_topics_filter(self, input: List[str]) -> List[str]:
        pass

    @abstractmethod
    async def exercises_filter(self, input: List[str]) -> List[str]:
        pass


@dataclass
class ItemFiltererArgs:
    subjects: Optional[List[str]] = None
    authors: Optional[List[str]] = None
    specifications: Optional[List[str]] = None
    years: Optional[List[int]] = None
    main_topics: Optional[List[str]] = None
    sub_topics: Optional[List[str]] = None
    sub_sub_topics: Optional[List[str]] = None
    exercises: Optional[List[str]] = None


class ItemFilterer(ItemFiltererI):
    def __init__(self, args: ItemFiltererArgs):
        self.subjects = args.subjects
        self.authors = args.authors
        self.specifications = args.specifications
        self.years = args.years
        self.main_topics = args.main_topics
        self.sub_topics = args.sub_topics
        self.sub_sub_topics = args.sub_sub_topics
        self.exercises = args.exercises

    def _filter(self, filtering_items, filter_items):
        if filter_items is None:
            return filtering_items
        return [i for i in filtering_items if i not in filter_items]

    async def subjects_filter(self, input: List[str]) -> List[str]:
        return self._filter(input, self.subjects)

    async def authors_filter(self, input: List[str]) -> List[str]:
        return self._filter(input, self.authors)

    async def specifications_filter(self, input: List[str]) -> List[str]:
        return self._filter(input, self.specifications)

    async def years_filter(self, input: List[int]) -> List[int]:
        return self._filter(input, self.years)

    async def main_topics_filter(self, input: List[str]) -> List[str]:
        return self._filter(input, self.main_topics)

    async def sub_topics_filter(self, input: List[str]) -> List[str]:
        return self._filter(input, self.sub_topics)

    async def sub_sub_topics_filter(self, input: List[str]) -> List[str]:
        return self._filter(input, self.sub_sub_topics)

    async def exercises_filter(self, input: List[str]) -> List[str]:
        return self._filter(input, self.exercises)
