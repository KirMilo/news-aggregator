import json
from typing import Annotated, AsyncGenerator

from aio_pika.abc import ExchangeType, AbstractQueue, AbstractIncomingMessage, AbstractConnection
from fastapi import Depends, Path
from starlette.websockets import WebSocket

from rabbit.exceptions import MessageQueueException
from rabbit.rmq_connection import get_rabbit_connection


class NewsCommentsMessagesQueue:
    def __init__(
            self,
            connection: AbstractConnection,
            news_id: int,
    ):
        self._connection = connection
        self._routing_key = f"comments.{news_id}"
        self._prefetch_count = 1
        self._queue: AbstractQueue | None = None
        self._websocket: WebSocket | None = None

    async def build_queue(
            self,
    ):
        channel = await self._connection.channel()
        await channel.set_qos(
            prefetch_count=self._prefetch_count,
        )
        exchange = await channel.declare_exchange(
            "comments_exchange",
            type=ExchangeType.TOPIC,
        )
        queue = await channel.declare_queue(
            exclusive=True,
        )
        await queue.bind(
            exchange,
            routing_key=self._routing_key,
        )
        self._queue = queue

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


async def get_news_comments_messages_queue(
        news_id: Annotated[int, Path(title="News ID")],
        connection: AbstractConnection = Depends(get_rabbit_connection),
) -> AsyncGenerator[NewsCommentsMessagesQueue, None]:
    queue = NewsCommentsMessagesQueue(connection, news_id)
    await queue.build_queue()
    yield queue
