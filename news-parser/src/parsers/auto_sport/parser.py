from parsers.base_parser import ParserBase
from parsers.auto_sport.handlers import FeedHandler, ItemHandler


class Parser(ParserBase):
    feed_urls = "https://www.championat.com/news/auto/1.html"
    feed_handler = FeedHandler
    items_handler = ItemHandler


# if __name__ == '__main__':
#     from schemas import Source
#     import datetime
#     from constants import UTC_PLUS_3
#
#     parser = Parser(
#         Source(
#             id=1,
#             link="https://www.championat.com/news/auto/1.html",
#             updated_at=datetime.datetime(2025, 9, 6, 15, 10, tzinfo=UTC_PLUS_3),
#         ),
#     )
#
#     print(parser.is_supported("https://www.championat.com/news/auto/1.html"))
#     parser.parse()
#     print(parser.parsed_data)
#     for data in parser.parsed_data.data:
#         print(data)
