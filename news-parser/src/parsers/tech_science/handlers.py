from datetime import datetime
from parsers.base_handlers import FeedHandlerBase, ItemHandlerBase
from schemas import ProcessingNews


class FeedHandler(FeedHandlerBase):
    __prefix = "https://lenta.ru"

    @staticmethod
    def _get_datetime(date: str, time: str) -> datetime:
        date = "-".join(date.split("/")[2:5])
        time = time.split(", ")[0]
        return datetime.fromisoformat(date + "T" + time)

    def handle(self):
        data = (
            self.data
            .find("ul", class_="rubric-page__container _subrubric")
            .find_all("li", class_="rubric-page__item _news", recursive=False)
        )
        items = []
        for item in data:
            items.append(
                ProcessingNews(
                    title=item.a.h3.text.strip(),
                    link=self.__prefix + item.a.get("href"),
                    published_at=self._get_datetime(
                        item.a.get("href"),
                        item.a.find("time").text.strip(),
                    )
                )
            )

        return items

class ItemHandler(ItemHandlerBase):
    def handle(self):
        paragraphs = (
            self.data
            .find("div", class_="topic-page__content _news")
            .find("div", class_="topic-body__content")
            .find_all("p", recursive=False)
        )
        return "\n\n".join(p.text.strip() for p in paragraphs)
