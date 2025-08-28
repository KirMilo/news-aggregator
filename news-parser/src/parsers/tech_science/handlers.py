from typing import List

from parsers.interfaces import FeedHandlerInterface, ItemHandlerInterface
from schemas import ProcessingNews


class FeedHandler(FeedHandlerInterface):
    def handle(self) -> List[ProcessingNews]:
        pass


class ItemHandler(ItemHandlerInterface):
    def handle(self) -> str:
        pass
