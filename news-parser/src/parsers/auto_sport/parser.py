from parsers.base_parser import ParserBase
from parsers.auto_sport.handlers import FeedHandler, ItemHandler


class Parser(ParserBase):
    feed_urls = "https://www.championat.com/news/auto/1.html"
    feed_handler = FeedHandler
    items_handler = ItemHandler

if __name__ == '__main__':
    from schemas import Resource, Source
    import datetime

    parser = Parser(
        Resource(
            source=Source(
                id=1,
                link="https://www.championat.com/news/auto/1.html",
                updated_at=datetime.datetime(2025, 8, 24, 15, 10),
            ),
            categories=[]
        )
    )

    print(parser.is_supported("https://www.championat.com/news/auto/1.html"))
    parser.parse()
    for data in parser.parsed_data.data:
        print(data)
