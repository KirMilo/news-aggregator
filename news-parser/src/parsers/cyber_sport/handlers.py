from datetime import datetime

from schemas import News
from parsers.base_handlers import FeedHandlerBase, ItemHandlerBase


class FeedHandler(FeedHandlerBase):
    def __init__(self, data: dict[str, ...], prefix: str):  # noqa
        self.data = data
        self.link_prefix = prefix + "/"

    def handle(self):
        items = []
        for item in self.data["data"]:
            item = item["attributes"]
            items.append(
                News(
                    title=item["title"],
                    link=self.link_prefix + item["slug"],
                    published_at=datetime.fromtimestamp(item["publishedAt"], tz=self.tz)
                )
            )

        return items


class ItemHandler(ItemHandlerBase):
    def handle(self):
        soup = (
            self.data
            .find("main")
            .find("article")
            .find(
                "div",
                class_="text-content js-mediator-article js-mediator-article root_sK2zH content_5HuK5",
            )
        )
        paragraphs = []
        for tag in soup.find_all(recursive=False):
            if tag.name == "p":
                paragraphs.append(tag.text)
            elif tag.name == "div" and not tag.has_attr("class") and tag.find("a", recursive=False):

                author = tag.a.find("span").text.strip() + "\n" + tag.a.find("small").text.strip()
                text = f"{author}\n<<{tag.p.text.strip()}>>"
                paragraphs.append(text)

        return "\n\n".join(paragraphs)
