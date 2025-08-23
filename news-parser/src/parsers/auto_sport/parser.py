from parsers.base_parser import ParserBase

from parsers.auto_sport.handlers import FeedHandler, ItemHandler


class Parser(ParserBase):
    feed_urls = "https://www.championat.com/news/auto/1.html"
    feed_handler = FeedHandler
    items_handler = ItemHandler
