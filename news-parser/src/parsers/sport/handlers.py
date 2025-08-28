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
            .find_all("a", recursive=False)
        )
        items = []
        for item in data:
            items.append(
                ProcessingNews(
                    link=item.get("href"),
                    title=item.span.text.strip(),
                    published_at=self._get_datetime(
                        item.find("span", class_="news-feed__item__date").text.strip()
                    )
                )
            )
        return items

class ItemHandler(ItemHandlerBase):
    def handle(self):
        data = (
            self.data
            .find("div", class_="article__text article__text_free")
            .find_all("p", recursive=False)
        )
        paragraphs = []
        for p in data:
            p = p.text.strip()
            if p:
                paragraphs.append(p)
        return "\n\n".join(paragraphs)
