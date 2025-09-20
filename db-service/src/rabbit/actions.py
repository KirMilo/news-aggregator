from pika.exchange_type import ExchangeType

from rabbit.base import RabbitMQChannel
from rabbit.messages import AbstractMessage


def publish_message(message: AbstractMessage):
    with RabbitMQChannel() as channel:
        channel.exchange_declare(
            exchange=message.exchange,
            exchange_type=ExchangeType.topic,
        )
        channel.basic_publish(
            routing_key=message.routing_key,
            exchange=message.exchange,
            body=message.message,
        )

def publish_messages(messages: list[AbstractMessage]):
    with RabbitMQChannel() as channel:
        for message in messages:
            channel.exchange_declare(
                exchange=message.exchange,
                exchange_type=ExchangeType.topic,
            )
            channel.basic_publish(
                routing_key=message.routing_key,
                exchange=message.exchange,
                body=message.message,
            )
