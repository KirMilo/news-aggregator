from datetime import datetime, timedelta

from parsers.base_handlers import FeedHandlerBase
from schemas import News


class FeedHandler(FeedHandlerBase):
    tz = str(FeedHandlerBase.tz)[3:]

    def _get_datetime(self, dt: str) -> datetime:
        dt = dt.split(",\xa0")
        today = datetime.now().date()
        if len(dt) > 2:
            today -= timedelta(days=1)
        return datetime.fromisoformat(str(today) + "T" + dt[-1] + self.tz)

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
                News(
                    link=item.get("href"),
                    title=item.span.text.strip(),
                    published_at=self._get_datetime(
                        item.find("span", class_="news-feed__item__date").span.text.strip()
                    )
                )
            )
        return items