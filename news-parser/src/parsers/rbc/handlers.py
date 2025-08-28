from datetime import datetime, timedelta

from parsers.base_handlers import FeedHandlerBase, ItemHandlerBase
from schemas import ProcessingNews


class FeedHandler(FeedHandlerBase):
    @staticmethod
    def _get_datetime(dt: str) -> datetime:
        dt = dt.split(",\xa0")
        today = datetime.now().date()
        if len(dt) > 2:
            today -= timedelta(days=1)
        return datetime.fromisoformat(str(today) + "T" + dt[-1])

    def handle(self):
        data = (
            self.data
            .find("div", class_="js-news-feed-list")
            .find_all(
                "a",
                class_="news-feed__item js-visited js-news-feed-item js-yandex-counter",
                recursive=False
            )
        )
        items = []
        for item in data:
            items.append(
                ProcessingNews(
                    link=item.get("href"),
                    title=item.span.text.strip(),
                    published_at=self._get_datetime(
                        item.find("span", class_="news-feed__item__date").span.text.strip()
                    )
                )
            )
        return items

class ItemHandler(ItemHandlerBase):
    def handle(self):
        data = (
            self.data
            .find("div", class_="article__text article__text_free")
            .find_all(recursive=False)
        )
        paragraphs = []
        for tag in data:
            if tag.name == "p" or tag.name == "h2":
                paragraph = tag.text.strip()
                if tag:
                    paragraphs.append(f"<b>{paragraph}</b>" if tag.name == "h2" else paragraph)
        return "\n\n".join(paragraphs)
