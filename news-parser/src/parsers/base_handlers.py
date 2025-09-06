from abc import ABC
from typing import Dict, Any, Callable
from bs4 import BeautifulSoup

from constants import UTC_PLUS_3
from parsers.interfaces import FeedHandlerInterface, ItemHandlerInterface, HandlerInterface


class UnprocessableData(Exception):
    pass


def try_parse_wrapper(func: Callable):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            raise UnprocessableData
    return wrapper


class HandlerBase(HandlerInterface, ABC):
    def __init__(self, data: str | Dict[str, Any]):
        self.data = BeautifulSoup(data, "lxml")


class FeedHandlerBase(HandlerBase, FeedHandlerInterface, ABC):
    tz = UTC_PLUS_3


class ItemHandlerBase(HandlerBase, ItemHandlerInterface, ABC):
    pass
