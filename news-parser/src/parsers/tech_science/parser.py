from parsers.base_parser import ParserBase
from parsers.tech_science.handlers import FeedHandler, ItemHandler


class Parser(ParserBase):
    feed_urls = [
        "https://lenta.ru/rubrics/science/science/",
        "https://lenta.ru/rubrics/science/digital/",
        "https://lenta.ru/rubrics/science/future/",
        "https://lenta.ru/rubrics/science/cosmos/",
    ]
    feed_handler = FeedHandler
    items_handler = ItemHandler


if __name__ == "__main__":
    from schemas import Resource, Source
    import datetime

    parser = Parser(
        Resource(
            source=Source(
                id=1,
                link="https://lenta.ru/rubrics/science/digital/",
                updated_at=datetime.datetime(2025, 8, 29, 19, 10),
            ),
            categories=[]
        )
    )

    print(parser.is_supported("https://lenta.ru/rubrics/science/digital/"))
    parser.parse()
    for data in parser.parsed_data:
        print(data)
