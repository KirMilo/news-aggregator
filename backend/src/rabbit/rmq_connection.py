from aio_pika.abc import AbstractConnection
from aio_pika import connect_robust

RABBITMQ_HOST = "localhost"
RABBITMQ_PORT = 5672
RABBITMQ_USER = "guest"
RABBITMQ_PASSWORD = "guest"


class RabbitConnection:
    _connection: AbstractConnection | None = None
    _consumers_count: int = 0

    async def get_connection(self) -> AbstractConnection:
        if self._connection is None:
            self._connection = await connect_robust(
                host=RABBITMQ_HOST,
                port=RABBITMQ_PORT,
                user=RABBITMQ_USER,
                password=RABBITMQ_PASSWORD,
            )
        return self._connection

    async def __aenter__(self) -> AbstractConnection:
        self._consumers_count += 1
        return await self.get_connection()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self._consumers_count -= 1
        if not self._consumers_count:
            await self._connection.close()
            self._connection = None
