import pika
from pika.adapters.blocking_connection import BlockingChannel

from core.settings import RABBIT_SETTINGS


class RabbitMQChannel:
    def __init__(self, connection_params: dict[str, str] = RABBIT_SETTINGS):
        self.connection_params = pika.ConnectionParameters(
            host=connection_params["host"],
            port=int(connection_params["port"]),
            credentials=pika.PlainCredentials(
                connection_params["user"],
                connection_params["password"],
            ),
        )
        self._connection: pika.BlockingConnection | None = None
        self._channel: BlockingChannel | None = None

    def __enter__(self) -> BlockingChannel:
        self._connection = pika.BlockingConnection(self.connection_params)
        self._channel = self._connection.channel()
        return self._channel

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._channel.close()
        self._connection.close()
