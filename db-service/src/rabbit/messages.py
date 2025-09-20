import json
from abc import ABC

from django.db.models import TextChoices
from rest_framework import serializers


class MessageActionType(TextChoices):
    NEW = "new"
    UPDATE = "update"
    DELETE = "delete"


class Message(serializers.Serializer):
    action = serializers.ChoiceField(choices=MessageActionType.choices)  # noqa
    value = serializers.IntegerField()

    def serial(self) -> bytes:
        self.is_valid(raise_exception=True)
        return json.dumps(self.validated_data).encode("utf-8")


class AbstractMessage(ABC):
    _exchange: str

    def __init__(self, topic: str, value: int, action: str = "new"):
        self._topic = topic
        self._message = Message(data={"action": action, "value": value})

    @property
    def exchange(self) -> str:
        return f"{self._exchange}_exchange"

    @property
    def routing_key(self) -> str:
        return f"{self._exchange}.{self._topic}"

    @property
    def message(self) -> bytes:
        return self._message.serial()


class NewsMessage(AbstractMessage):
    _exchange = "news"


class CommentMessage(AbstractMessage):
    _exchange = "comments"
