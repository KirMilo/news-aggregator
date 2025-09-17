from datetime import datetime, timedelta

from parsers.base_handlers import FeedHandlerBase, ItemHandlerBase
from schemas import News


class FeedHandler(FeedHandlerBase):
    tz = str(FeedHandlerBase.tz)[3:]

    def _get_datetime(self, dt: str) -> datetime:
        dt = dt.split(", ")
        today = datetime.now().date()
        if len(dt) > 2:
            today -= timedelta(days=1)
        return datetime.fromisoformat(str(today) + "T" + dt[-1] + self.tz)

    def handle(self):
        data = (
            self.data
            .find("div", class_="l-row js-load-container")
            .find_all(
                "div",
                class_="item__wrap l-col-center",
            )
        )
        items = []
        for item in data:
            a = item.find("a", recursive=False)

            items.append(
                News(
                    link=a.get("href"),
                    title=a.find("span", class_="normal-wrap").text.strip(),
                    published_at=self._get_datetime(
                        item.find("div", class_="item__bottom").span.text.strip(),
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
