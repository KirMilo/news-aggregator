from parsers.base_parser import ParserBase
from parsers.rbc.handlers import FeedHandler, ItemHandler


class Parser(ParserBase):
    feed_urls = [
        "https://sportrbc.ru/",
        "https://www.rbc.ru/politics/",
        "https://www.rbc.ru/economics/",
        "https://www.rbc.ru/finances/",
        "https://www.rbc.ru/technology_and_media/",
    ]
    feed_handler = FeedHandler
    items_handler = ItemHandler
    __white_list = [
        "https://www.rbc.ru/",
        "https://sportrbc.ru/",
        "https://nn.rbc.ru/",
    ]

    def _filter_items(self, items):
        items = filter(
            lambda item: any(str(item.link)[:len(prefix)] == prefix for prefix in self.__white_list),
            items,
        )
        return super()._filter_items(items)


if __name__ == "__main__":
    from schemas import Resource, Source
    import datetime

    parser = Parser(
        Resource(
            source=Source(
                id=1,
                link="https://www.rbc.ru/economics/",
                updated_at=datetime.datetime(2025, 8, 28, 19, 10),
            ),
            categories=[]
        )
    )

    print(parser.is_supported("https://sportrbc.ru/"))
    parser.parse()
    for data in parser.parsed_data:
        print(data)
