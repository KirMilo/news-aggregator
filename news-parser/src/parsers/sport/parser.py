from parsers.base_parser import ParserBase
from parsers.sport.handlers import FeedHandler, ItemHandler


class Parser(ParserBase):
    feed_urls = "https://sportrbc.ru/"
    feed_handler = FeedHandler
    items_handler = ItemHandler


if __name__ == "__main__":
    from schemas import Resource, Source
    import datetime

    parser = Parser(
        Resource(
            source=Source(
                id=1,
                link="https://sportrbc.ru/",
                updated_at=datetime.datetime(2025, 8, 28, 18, 10),
            ),
            categories=[]
        )
    )

    print(parser.is_supported("https://sportrbc.ru/"))
    parser.parse()
    for data in parser.parsed_data:
        print(data)
