from aio_pika import ExchangeType
from aio_pika.abc import AbstractIncomingMessage

from rmq_connection import RabbitConnection


class NewsChannel:
    async def on_message(self, message: AbstractIncomingMessage):
        """Обработка полученного сообщения"""
        """Пересылка сообщения в ручку"""

    async def get_channel(self):
        async with RabbitConnection() as connection:
            channel = await connection.channel()
            await channel.set_qos(prefetch_count=1)

            news_exchange = await channel.declare_exchange(
                name="news",
                type=ExchangeType.FANOUT,
            )

            queue = await channel.declare_queue(exclusive=True)

            await queue.bind(news_exchange)
            await queue.consume(self.on_message)
