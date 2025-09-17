from parsers.rbc.parser import Parser as RBCParser
from parsers.sport_rbc.handlers import FeedHandler


class Parser(RBCParser):
    feed_urls = "https://sportrbc.ru/"
    feed_handler = FeedHandler


# if __name__ == '__main__':
#     from schemas import Source
#     import datetime
#     from constants import UTC_PLUS_3
#
#     parser = Parser(
#         Source(
#             id=1,
#             link="https://sportrbc.ru/",
#             updated_at=datetime.datetime(2025, 9, 6, 15, 10, tzinfo=UTC_PLUS_3),
#         ),
#     )
#
#     print(parser.is_supported("https://sportrbc.ru/"))
#     parser.parse()
#     print(parser.parsed_data)
#     for data in parser.parsed_data.data:
#         print(data)