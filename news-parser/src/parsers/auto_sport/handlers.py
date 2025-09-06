from datetime import datetime

from schemas import News
from parsers.base_handlers import FeedHandlerBase, ItemHandlerBase

MONTHS = {
    "января": "01",
    "февраля": "02",
    "марта": "03",
    "апреля": "04",
    "мая": "05",
    "июня": "06",
    "июля": "07",
    "августа": "08",
    "сентября": "09",
    "октября": "10",
    "ноября": "11",
    "декабря": "12",
}


class FeedHandler(FeedHandlerBase):
    __prefix = "https://www.championat.com"

    def _get_datetime(self, date: str, time: str) -> datetime:
        dt_list = date.strip().lower().split(" ")[::-1] + time.strip().split(":")
        dt_list[1] = MONTHS[dt_list[1]]
        return datetime(*map(lambda i: int(i), dt_list), tzinfo=self.tz)

    def handle(self):
        soup = (self.data
                .body.find("div", {"class": "page"})
                .find("div", {"class": "page-content"})
                .find("div", {"class": "page-main"})
                .find("div", {"class": "news _all"})
                .div
                )
        date = soup.div.text

        items = []
        for item in soup.find_all("div", {"class": "news-item"}):
            a = item.find("a")
            items.append(
                News(
                    published_at=self._get_datetime(date, item.div.text),
                    title=a.text,
                    link=self.__prefix + a.attrs["href"],
                )
            )
        return items


class ItemHandler(ItemHandlerBase):
    def handle(self):
        soup = self.data.find("div", {"class": "article-content"})
        paragraphs = soup.find_all("p", recursive=False)
        return "\n\n".join(p.text.strip() for p in paragraphs)
