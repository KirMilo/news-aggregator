from httpx import Client as HttpxClient
from typing import List, Dict, Any

from constants import DB_SERVICE_URL, RESOURCES_ENDPOINT_GET, CREATE_NEWS_ENDPOINT_POST
from schemas import Source, CreateNews
from parsers import ParserInterface, PARSERS_CLASSES


class NewsParser:
    def __init__(self):
        self.db_service_url = DB_SERVICE_URL
        self.resources_endpoint_get = RESOURCES_ENDPOINT_GET
        self.create_news_endpoint_post = CREATE_NEWS_ENDPOINT_POST
        self.sources = [Source(**source) for source in self._get_sources()]
        self.parsers = self._get_parsers()
        self.output_data = None

    def _get_parsers(self) -> List[ParserInterface]:
        parsers = []
        for source in self.sources:
            url = str(source.link)
            for parser_class in PARSERS_CLASSES:
                if parser_class.is_supported(url):
                    parsers.append(parser_class(source))
        return parsers

    def _get_sources(self) -> List[Dict[str, Any]]:  # noqa
        with HttpxClient(
                base_url=self.db_service_url,
        ) as client:
            response = client.get(self.resources_endpoint_get)
            response.raise_for_status()
            return response.json()

    def parse(self):
        for parser in self.parsers:
            parser.parse()
        self.output_data = [parser.parsed_data for parser in self.parsers if parser.parsed_data]

    def create_news(self):
        with HttpxClient(
                base_url=self.db_service_url,
        ) as client:
            response = client.post(
                url=self.create_news_endpoint_post,
                json=CreateNews(data=self.output_data).model_dump(),
            )
            response.raise_for_status()
