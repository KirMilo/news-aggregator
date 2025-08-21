from datetime import datetime, timezone, timedelta
from abc import ABC

from parsers.interfaces import ParserInterface
from schemas import Resource, ParsedNews

UTC_PLUS_3 = timezone(timedelta(hours=3))


class ParserBase(ParserInterface, ABC):
    headers = {}

    def __init__(self, resource: Resource):
        self._resource = resource
        self._updated_at = resource.source.updated_at
        self._data = None

    # TODO: Доделать методы
    def _parse_feed(self):
        pass

    def _filter_items(self, items):
        pass

    def _parse_items(self, items):
        pass

    def parse(self):
        feed = self._parse_feed()
        self._resource.source.updated_at = datetime.now(tz=UTC_PLUS_3)
        items = self.feed_handler(feed).handle()
        filtered_items = self._filter_items(items)
        parsed_items = self._parse_items(filtered_items)
        self._data = self.items_handler(parsed_items).handle()

    @property
    def parsed_data(self) -> ParsedNews | None:
        if self._data:
            return ParsedNews(
                **self._resource.model_dump(),
                data=self._data,
            )
        return None

    def is_processed(self, link: str) -> bool:
        if isinstance(self.feed_urls, str):
            return link == self.feed_urls
        else:
            return link in self.feed_urls
