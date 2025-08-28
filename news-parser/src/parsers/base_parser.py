from httpx import (
    Client as HttpxClient,
    Response as HttpxResponse,
)
from enum import Enum
from datetime import datetime, timezone, timedelta
from abc import ABC
from typing import List, Dict, Any, Iterable

from parsers.interfaces import ParserInterface
from schemas import Resource, ParsedNews, News, ProcessingNews

UTC_PLUS_3 = timezone(timedelta(hours=3))


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

    def __init__(self, resource: Resource):
        self.parse_feed_strategy = ParseDataStrategy(self.parse_feed_strategy)
        self.parse_items_strategy = ParseDataStrategy(self.items_feed_strategy)
        self._resource = resource
        self._feed_url = resource.source.link
        self._updated_at = resource.source.updated_at
        self._data = None

    def _get_source_data(self, url: str) -> HttpxResponse:
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

    def _filter_items(self, items: Iterable[ProcessingNews]) -> List[News]:
        filtered_items = []
        for item in items:
            if item.published_at <= self._updated_at:
                break
            filtered_items.append(News(**item.model_dump()))
        return filtered_items

    def _get_item_data(self, url: str) -> str | None:
        response = self._get_source_data(url)
        if self.parse_items_strategy is ParseDataStrategy.HTML:
            return response.content.decode("utf-8")
        else:
            return response.json()

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
        self._resource.source.updated_at = datetime.now(tz=UTC_PLUS_3)
        items = self.feed_handler(feed).handle()
        filtered_items = self._filter_items(items)
        parsed_news = self._parse_news(filtered_items)
        self._data = parsed_news

    @property
    def parsed_data(self) -> ParsedNews | None:
        if self._data:
            return ParsedNews(
                **self._resource.model_dump(),
                data=self._data,
            )
        return None

    def is_supported(self, link: str) -> bool:
        if isinstance(self.feed_urls, str):
            return link == self.feed_urls
        else:
            return link in self.feed_urls
