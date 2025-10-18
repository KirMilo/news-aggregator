from typing import AsyncGenerator

from aio_pika.abc import AbstractConnection
from aio_pika import connect_robust

RABBITMQ_HOST = "localhost"
RABBITMQ_PORT = 5672
RABBITMQ_USER = "guest"
RABBITMQ_PASSWORD = "guest"


class RabbitConnection:
    _connection: AbstractConnection | None = None
    _consumers_count: int = 0

    @classmethod
    def _inc_consumers(cls):  # noqa
        cls._consumers_count += 1

    @classmethod
    def _dec_consumers(cls):
        cls._consumers_count -= 1

    @classmethod
    async def _get_connection(cls) -> AbstractConnection:
        if cls._connection is None:
            cls._connection = await connect_robust(
                host=RABBITMQ_HOST,
                port=RABBITMQ_PORT,
                user=RABBITMQ_USER,
                password=RABBITMQ_PASSWORD,
            )
        return cls._connection

    @classmethod
    async def _unset_connection(cls):
        await cls._connection.close()
        cls._connection = None

    async def __aenter__(self) -> AbstractConnection:
        if not self._consumers_count:
            self._connection = await self._get_connection()
        self._inc_consumers()
        return self._connection

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self._dec_consumers()
        if not self._consumers_count:
            await self._unset_connection()


async def get_rabbit_connection() -> AsyncGenerator[AbstractConnection, None]:
    async with RabbitConnection() as connection:
        yield connection
