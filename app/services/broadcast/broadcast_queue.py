import typing
import aio_pika
import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.utils.executor import Executor
from app import config
from app.services.admin import send_message_catching_errors
from app.services.broadcast.interface import Consumer, Publisher

from app.config import (
    RABBITMQ_HOST,
    RABBITMQ_PORT,
    RABBITMQ_USER,
    RABBITMQ_PASSWORD,
    RABBITMQ_QUEUE_NAME,
    RABBITMQ_EXCHANGE_NAME,
)

BROADCAST_MESSAGE_FORMAT = "{user_id}:{message_id}"
END_OF_BROADCAST_MESSAGE = "end_of_broadcast"
END_OF_BROADCAST_MESSAGE_ENCODED = END_OF_BROADCAST_MESSAGE.encode()


class BroadcastPublisher(Publisher):
    def __init__(
        self,
        exchange_name: str,
        queue_name: str,
        connection: typing.Optional[aio_pika.abc.AbstractRobustConnection] = None,
    ):
        self.queue_name = queue_name
        self.exchange_name = exchange_name
        self.connection = connection

        self.channel: typing.Optional[aio_pika.abc.AbstractChannel] = None
        self.exchange: typing.Optional[aio_pika.abc.AbstractExchange] = None

    async def _setup(self):
        if not self.connection:
            self.connection = await aio_pika.connect_robust(
                host=RABBITMQ_HOST,
                port=RABBITMQ_PORT,
                login=RABBITMQ_USER,
                password=RABBITMQ_PASSWORD,
            )
        if not self.channel:
            self.channel = await self.connection.channel(publisher_confirms=False)
            self.exchange = await self.channel.declare_exchange(self.exchange_name)
            await self.channel.declare_queue(self.queue_name)

    async def publish(
        self, user_id: typing.Union[int, str], message_id: typing.Union[int, str]
    ):
        await self._setup()

        await self.exchange.publish(
            aio_pika.Message(
                body=f"{user_id}:{message_id}".encode(),
            ),
            routing_key=self.queue_name,
        )

    async def publish_end_of_broadcast(self):
        await self.exchange.publish(
            aio_pika.Message(body=END_OF_BROADCAST_MESSAGE_ENCODED),
            routing_key=self.queue_name,
        )

    async def close(self):
        if self.connection:
            await self.connection.close()
        if self.channel:
            await self.channel.close()


class BroadcastConsumer(Consumer):
    def __init__(
        self,
        exchange_name: str,
        queue_name: str,
        *,
        bot: typing.Optional[Bot] = None,
        connection: typing.Optional[aio_pika.abc.AbstractRobustConnection] = None,
    ):
        self.queue_name = queue_name
        self.exchange_name = exchange_name
        self.connection = connection
        self.bot = bot

        self.channel: typing.Optional[aio_pika.abc.AbstractChannel] = None
        self.queue: typing.Optional[aio_pika.abc.AbstractQueue] = None
        self.exchange: typing.Optional[aio_pika.abc.AbstractExchange] = None

        self.lock = asyncio.Lock()
        self.sent_messages_count = 0

    async def _setup(self):
        if not self.connection:
            self.connection = await aio_pika.connect_robust(
                host=RABBITMQ_HOST,
                port=RABBITMQ_PORT,
                login=RABBITMQ_USER,
                password=RABBITMQ_PASSWORD,
            )
        if not self.channel:
            self.channel = await self.connection.channel()
            self.queue = await self.channel.declare_queue(self.queue_name)
            self.exchange = await self.channel.declare_exchange(self.exchange_name)
            await self.queue.bind(self.exchange, routing_key=self.queue_name)

        await self.channel.set_qos(prefetch_count=1)

    async def start_consume(self):
        await self._setup()
        await self.queue.consume(self.on_message)

    async def on_message(self, message: aio_pika.abc.AbstractIncomingMessage):
        body = message.body.decode()
        try:
            # TOOD: rate limiter
            await self.process_message(body)
            await message.ack()
        except Exception as e:
            # TODO: max 5 retries
            # TODO: logging
            print(f"{body=} {e=}")
            await message.nack(requeue=True)

    async def process_message(self, body: str):
        if body == END_OF_BROADCAST_MESSAGE:
            await self.bot.send_message(
                config.ADMIN_ID,
                config.MSG_SUCCESSFUL_SEND_ALL.format(self.sent_messages_count),
            )
            async with self.lock:
                self.sent_messages_count = 0
            return
        elif len(body.split(":")) != 2:
            return

        user_id, message_id = body.split(":")
        msg = types.Message(
            bot=self.bot,
            message_id=int(message_id),
            chat=types.Chat(id=config.ADMIN_ID),
        )

        _, error = await send_message_catching_errors(user_id, msg)
        if error:
            return
        async with self.lock:
            self.sent_messages_count += 1

    async def close(self):
        if self.connection:
            await self.connection.close()
        if self.channel:
            await self.channel.close()


broadcast_publisher = BroadcastPublisher(RABBITMQ_EXCHANGE_NAME, RABBITMQ_QUEUE_NAME)
broadcast_consumer = BroadcastConsumer(RABBITMQ_EXCHANGE_NAME, RABBITMQ_QUEUE_NAME)


async def connect_to_rabbitmq() -> aio_pika.abc.AbstractRobustConnection:
    return await aio_pika.connect_robust(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        login=RABBITMQ_USER,
        password=RABBITMQ_PASSWORD,
    )


async def on_startup(dispatcher: Dispatcher):
    conn = await connect_to_rabbitmq()
    broadcast_publisher.connection = conn
    broadcast_consumer.connection = conn
    broadcast_consumer.bot = dispatcher.bot
    await broadcast_consumer.start_consume()


async def on_shutdown(dispatcher: Dispatcher):
    await broadcast_publisher.close()
    await broadcast_consumer.close()


def setup(runner: Executor):
    runner.on_startup(on_startup)
    runner.on_shutdown(on_shutdown)
