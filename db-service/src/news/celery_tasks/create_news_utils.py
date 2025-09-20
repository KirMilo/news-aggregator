from collections import defaultdict
from django.contrib.postgres.aggregates import ArrayAgg
from news.models import Source
from rabbit.messages import NewsMessage


def get_sources_categories() -> dict[int, list[str]]:
    queryset = (
        Source
        .objects
        .prefetch_related("categories")
        .values("id")
        .annotate(categories=ArrayAgg("categories__slug"))
    )
    return {item["id"]: item["categories"] for item in queryset}


def get_categories_news(sources_news_count: dict[int, int]) -> dict[str, int]:
    sources_categories = get_sources_categories()
    categories_news = defaultdict(int)
    for source, news_count in sources_news_count.items():
        if news_count:
            for category in sources_categories[source]:
                categories_news[category] += news_count
    categories_news["all"] = sum(sources_news_count.values())
    return categories_news


def new_news_messages_to_broker(data: dict[int, int]) -> list[NewsMessage]:
    categories_news = get_categories_news(data)
    return [
        NewsMessage(
            topic=category,
            value=news_count
        ) for category, news_count in categories_news.items()
    ]
