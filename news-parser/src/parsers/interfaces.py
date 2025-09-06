from abc import ABC, abstractmethod
from typing import Type, List, Any, Dict

from schemas import ParsedNews, Source, News


class HandlerInterface(ABC):
    @abstractmethod
    def __init__(self, data: str | Dict[str, Any], *args, **kwargs):  # noqa
        pass

    @abstractmethod
    def handle(self) -> Any:
        pass


class FeedHandlerInterface(HandlerInterface, ABC):
    @abstractmethod
    def handle(self) -> List[News]:
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
    def __init__(self, source: Source):  # noqa
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
