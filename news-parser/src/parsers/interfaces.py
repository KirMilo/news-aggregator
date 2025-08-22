from abc import ABC, abstractmethod
from typing import Type, List, Any, Dict

from src.schemas import ParsedNews, Resource, ProcessingNews


class FeedHandlerInterface(ABC):
    def __init__(self, feed: str | Dict[str, Any]):
        self.feed = feed

    @abstractmethod
    def handle(self) -> List[ProcessingNews]:
        pass

class ItemHandlerInterface(ABC):
    def __init__(self, item: str | Dict[str, Any]):
        self.item = item

    @abstractmethod
    def handle(self) -> str:
        pass


class ParserInterface(ABC):
    feed_urls: str | List[str]
    feed_handler: Type[FeedHandlerInterface]
    items_handler: Type[ItemHandlerInterface]

    @abstractmethod
    def __init__(self, resource: Resource):
        self.resource = resource

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
