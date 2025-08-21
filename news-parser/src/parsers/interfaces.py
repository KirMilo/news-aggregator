from abc import ABC, abstractmethod
from typing import Type, List, Any

from schemas import ParsedNews, Resource


class HandlerInterface(ABC):
    @abstractmethod
    def handle(self):
        pass


class FeedHandlerInterface(HandlerInterface, ABC):
    @abstractmethod
    def __init__(self, feed):
        pass

class ItemHandlerInterface(HandlerInterface, ABC):
    @abstractmethod
    def __init__(self, item):
        pass


class ParserInterface(ABC):
    feed_urls: str | List[str]
    _headers: dict[str, Any]
    feed_handler: Type[FeedHandlerInterface]
    items_handler: Type[ItemHandlerInterface]


    @abstractmethod
    def __init__(self, resource: Resource):
        pass

    @abstractmethod
    def parse(self):
        pass

    @abstractmethod
    def _parse_feed(self):
        pass

    @abstractmethod
    def _filter_items(self, items):
        pass

    @abstractmethod
    def _parse_items(self, items):
        pass

    @property
    @abstractmethod
    def parsed_data(self) -> ParsedNews | None:
        pass

    @abstractmethod
    def is_processed(self, link: str) -> bool:
        pass
