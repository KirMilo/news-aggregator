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


# if __name__ == '__main__':
#     from schemas import Source
#     import datetime
#     from constants import UTC_PLUS_3
#
#     parser = Parser(
#         Source(
#             id=1,
#             link="https://lenta.ru/rubrics/science/cosmos/",
#             updated_at=datetime.datetime(2025, 9, 6, 12, 10, tzinfo=UTC_PLUS_3),
#         ),
#     )
#
#     print(parser.is_supported("https://lenta.ru/rubrics/science/cosmos/"))
#     parser.parse()
#     print(parser.parsed_data)
#     for data in parser.parsed_data.data:
#         print(data)