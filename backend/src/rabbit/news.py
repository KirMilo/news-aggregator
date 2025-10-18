import json
from contextlib import asynccontextmanager
from typing import Annotated, AsyncGenerator

from aio_pika.abc import ExchangeType, AbstractQueue, AbstractIncomingMessage, AbstractConnection
from fastapi import Query, Depends
from starlette.websockets import WebSocket

from rabbit.exceptions import MessageQueueException
from rabbit.rmq_connection import get_rabbit_connection


class NewsMessagesQueue:
    def __init__(
            self,
            connection: AbstractConnection,
            category: str,
    ):
        self._connection = connection
        self._routing_key = f"news.{category}"
        self._prefetch_count = 1
        self._queue: AbstractQueue | None = None
        self._websocket: WebSocket | None = None

    @asynccontextmanager
    async def channel(
            self,
    ):
        channel = await self._connection.channel()
        await channel.set_qos(
            prefetch_count=self._prefetch_count,
        )
        exchange = await channel.declare_exchange(
            "news_exchange",
            type=ExchangeType.TOPIC,
        )
        queue = await channel.declare_queue(
            exclusive=True,
            auto_delete=True,
        )
        await queue.bind(
            exchange,
            routing_key=self._routing_key,
        )
        self._queue = queue
        yield
        await channel.close()

    async def on_message(self, message: AbstractIncomingMessage):
        async with message.process():
            await self._websocket.send_json(
                json.loads(message.body)
            )

    def set_websocket(self, websocket: WebSocket):
        self._websocket = websocket

    def send_update_on_receipt(self):
        if not self._websocket:
            raise MessageQueueException("Websocket is not set for NewsMessagesQueue")
        return self._queue.consume(self.on_message)


async def get_news_messages_queue(
        category: Annotated[
            str,
            Query(title="Category", min_length=3, max_length=50)
        ] = "all",
        connection: AbstractConnection = Depends(get_rabbit_connection),
) -> AsyncGenerator[NewsMessagesQueue, None]:
    queue = NewsMessagesQueue(connection, category)
    async with queue.channel():
        yield queue
