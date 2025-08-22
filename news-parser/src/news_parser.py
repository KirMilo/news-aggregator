import httpx
from typing import List, Dict, Any

from src.constants import DB_SERVICE_URL, RESOURCES_ENDPOINT_GET, CREATE_NEWS_ENDPOINT_POST
from src.schemas import Resource
from parsers import ParserInterface, parsers


class NewsParser:
    def __init__(self):
        self.db_service_url = DB_SERVICE_URL
        self.resources_endpoint_get = RESOURCES_ENDPOINT_GET
        self.create_news_endpoint_post = CREATE_NEWS_ENDPOINT_POST
        self.resources = [Resource(**resource) for resource in self._get_resources()]
        self.parsers = self._get_parsers()
        self.news = None

    def _get_parsers(self) -> List[ParserInterface]:
        _parsers = []
        for resource in self.resources:
            url = str(resource.source.link)
            for parser in parsers:
                if parser.is_supported(url):
                    _parsers.append(parser(resource))
        return _parsers

    def _get_resources(self) -> List[Dict[str, Any]]:  # noqa
        with httpx.Client(
                base_url=self.db_service_url,
        ) as client:
            response = client.get(self.resources_endpoint_get)
            response.raise_for_status()
            return response.json()

    def parse(self):
        for parser in self.parsers:
            parser.parse()
        self.news = [parser.parsed_data for parser in self.parsers if parser.parsed_data]
        return self.news  # TODO: Протестировать и убрать эту строку

    def create_news(self):
        with httpx.Client(
                base_url=self.db_service_url,
        ) as client:
            response = client.post(
                url=self.create_news_endpoint_post,
                json=self.news
            )
            response.raise_for_status()
