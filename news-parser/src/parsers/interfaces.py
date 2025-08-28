from abc import ABC, abstractmethod
from typing import Type, List, Any, Dict

from schemas import ParsedNews, Resource, ProcessingNews


class HandlerInterface(ABC):
    @abstractmethod
    def __init__(self, data: str | Dict[str, Any], *args, **kwargs):  # noqa
        pass

    @abstractmethod
    def handle(self) -> Any:
        pass


class FeedHandlerInterface(HandlerInterface, ABC):
    @abstractmethod
    def handle(self) -> List[ProcessingNews]:
        pass

class ItemHandlerInterface(HandlerInterface, ABC):
    @abstractmethod
    def handle(self) -> str:
        pass


class ParserInterface(ABC):
    feed_urls: str | List[str]
    feed_handler: Type[FeedHandlerInterface]
    items_handler: Type[ItemHandlerInterface]

    @abstractmethod
    def __init__(self, resource: Resource):
        pass

    @abstractmethod
    def parse(self):
        pass

    @property
    @abstractmethod
    def parsed_data(self) -> ParsedNews | None:
        pass

    @abstractmethod
    def is_supported(self, link: str) -> bool:
        pass
