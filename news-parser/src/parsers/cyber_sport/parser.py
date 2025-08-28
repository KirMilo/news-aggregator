from functools import partial as functools_partial

from parsers.base_parser import ParserBase
from parsers.cyber_sport.handlers import FeedHandler, ItemHandler


TAGS_ID = {
    "dota-2": 103,
    "cs2": 10,
}


class Parser(ParserBase):
    feed_urls = ["https://www.cybersport.ru/tags/dota-2", "https://www.cybersport.ru/tags/cs2"]
    feed_handler = FeedHandler
    items_handler = ItemHandler
    parse_feed_strategy = "JSON"
    __ad_list = [
        "cybersport.ru",
        "сбер",
        "яндекс",
    ]

    def __init__(self, resource):
        super().__init__(resource)
        self.feed_handler = functools_partial(
            self.feed_handler,
            prefix=str(self._feed_url),
        )
        tag = str(self._feed_url)[str(self._feed_url).rfind("/") + 1:]
        if (tag_id := TAGS_ID.get(tag)) is None:
            raise NotImplementedError(f"Tag {tag} is not implemented")
        self._feed_url = (
            "https://www.cybersport.ru/api/materials"
            "?page[offset]=0"
            "&page[limit]=25"
            f"&filter[tagIds]={tag_id}"
            "&sort=internalRating"
        )

    def _filter_items(self, items):
        items = filter(
            lambda item: not any(ad in item.title.strip().lower() for ad in self.__ad_list),
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
                link="https://www.cybersport.ru/tags/dota-2",
                updated_at=datetime.datetime(2025, 8, 28, 16, 10),
            ),
            categories=[]
        )
    )

    print(parser.is_supported("https://www.cybersport.ru/tags/dota-2"))
    parser.parse()
    for data in parser.parsed_data:
        print(data)
