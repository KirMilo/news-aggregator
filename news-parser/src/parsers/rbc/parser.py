from parsers.base_parser import ParserBase
from parsers.rbc.handlers import FeedHandler, ItemHandler


class Parser(ParserBase):
    feed_urls = [
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
