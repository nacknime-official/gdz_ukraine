from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List


@dataclass
class Solution:
    id: int
    urls: List[str]


class IWrapper(ABC):
    @abstractmethod
    async def get_subjects(self) -> List[str]:
        pass

    @abstractmethod
    async def get_authors(self) -> List[str]:
        pass

    @abstractmethod
    async def get_specifications(self) -> List[str]:
        pass

    @abstractmethod
    async def get_years(self) -> List[int]:
        pass

    @abstractmethod
    async def get_main_topics(self) -> List[str]:
        pass

    @abstractmethod
    async def get_sub_topics(self) -> List[str]:
        pass

    @abstractmethod
    async def get_sub_sub_topics(self) -> List[str]:
        pass

    @abstractmethod
    async def get_exercises(self) -> List[str]:
        pass

    @abstractmethod
    async def get_solution(self) -> Solution:
        pass


class IWrapperForBot(ABC):
    @abstractmethod
    async def _init(self):
        pass

    @abstractmethod
    async def get_subjects(self, delete_data=False) -> List[str]:
        pass

    @abstractmethod
    async def get_authors(self, delete_data=False) -> List[str]:
        pass

    @abstractmethod
    async def get_specifications(self) -> List[str]:
        pass

    @abstractmethod
    async def get_years(self) -> List[int]:
        pass

    @abstractmethod
    async def get_main_topics(self, delete_data=False) -> List[str]:
        pass

    @abstractmethod
    async def get_sub_topics(self) -> List[str]:
        pass

    @abstractmethod
    async def get_sub_sub_topics(self) -> List[str]:
        pass

    @abstractmethod
    async def get_exercises(self) -> List[str]:
        pass

    @abstractmethod
    async def get_solution(self) -> Solution:
        pass
