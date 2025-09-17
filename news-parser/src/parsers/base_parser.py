from httpx import (
    Client as HttpxClient,
    Response as HttpxResponse,
)
from enum import Enum
from datetime import datetime
from abc import ABC
from typing import List, Dict, Any, Iterable

from parsers.interfaces import ParserInterface
from schemas import Source, ParsedNews, News, UpdatedSource
from constants import UTC_PLUS_3


class ParseDataStrategy(Enum):
    HTML = "HTML"
    JSON = "JSON"


class ParserBase(ParserInterface, ABC):
    headers = {
        "X-Service": "true",
        "Connection": "Keep-Alive",
        "User-Agent": "Android; 12; Google; google_pixel_27; 8.72.5; 13311234;"
    }
    timeout = 30
    parse_feed_strategy = "HTML"
    items_feed_strategy = "HTML"
    tz = UTC_PLUS_3

    def __init__(self, source: Source):
        self.parse_feed_strategy = ParseDataStrategy(self.parse_feed_strategy)
        self.parse_items_strategy = ParseDataStrategy(self.items_feed_strategy)
        self._source = source
        self._feed_url = source.link
        self.feed_url = self._feed_url
        self._data = None

    def _get_source_data(self, url: str) -> HttpxResponse:
        print(f"Getting {url}")  # TODO: Удалить в проде
        with HttpxClient(
                headers=self.headers,
                timeout=self.timeout,
                follow_redirects=True,
        ) as client:
            response = client.get(url)
            response.raise_for_status()
            return response

    def _parse_feed(self) -> str | Dict[str, Any] | None:
        response = self._get_source_data(str(self._feed_url))
        if self.parse_feed_strategy is ParseDataStrategy.HTML:
            return response.content.decode("utf-8")
        else:
            return response.json()

    def _filter_items(self, items: Iterable[News]) -> List[News]:
        filtered_items = []
        for item in items:
            if item.published_at <= self._source.updated_at:
                break
            filtered_items.append(item)
        return filtered_items

    def _get_item_data(self, url: str) -> str | None:
        try:
            response = self._get_source_data(url)
            if self.parse_items_strategy is ParseDataStrategy.HTML:
                return response.content.decode("utf-8")
            else:
                return response.json()
        except Exception as e:  # noqa
            return None


    def _parse_news(self, items: List[News]) -> List[News]:
        parsed_news = []
        for item in items:
            data = self._get_item_data(str(item.link))
            if data:
                item.body = self.items_handler(data).handle()
                parsed_news.append(item)
        return parsed_news

    def parse(self):
        feed = self._parse_feed()
        items = self.feed_handler(feed).handle()
        filtered_items = self._filter_items(items)
        self._source.updated_at = datetime.now(tz=self.tz)
        parsed_news = self._parse_news(filtered_items)
        self._data = parsed_news

    @property
    def parsed_data(self) -> ParsedNews | None:
        if self._data:
            return ParsedNews(
                source=UpdatedSource(**self._source.model_dump()),
                news=self._data,
            )
        return None

    @classmethod
    def is_supported(cls, link: str) -> bool:
        if isinstance(cls.feed_urls, str):
            return link == cls.feed_urls
        else:
            return link in cls.feed_urls
