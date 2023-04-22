from abc import ABC, abstractmethod

import typing


class Publisher(ABC):
    @abstractmethod
    async def publish(
        self, user_id: typing.Union[int, str], message_id: typing.Union[int, str]
    ):
        pass

    async def publish_end_of_broadcast(self):
        pass


class Consumer(ABC):
    @abstractmethod
    async def start_consume(self):
        pass
