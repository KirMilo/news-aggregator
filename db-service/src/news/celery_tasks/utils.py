from collections import defaultdict
from django.contrib.postgres.aggregates import ArrayAgg
from django_elasticsearch_dsl.registries import registry
from elasticsearch.dsl.connections import connections
from elasticsearch.helpers import bulk

from news.documents import NewsDocument
from news.models import Source, News
from rabbit.actions import publish_messages
from rabbit.messages import NewsMessage


class RabbitMQNews:
    @classmethod
    def _get_sources_categories(cls) -> dict[int, list[str]]:
        queryset = (
            Source
            .objects
            .prefetch_related("categories")
            .values("id")
            .annotate(categories=ArrayAgg("categories__slug"))
        )
        return {item["id"]: item["categories"] for item in queryset}

    @classmethod
    def _get_categories_news(cls, sources_news_count: dict[int, int]) -> dict[str, int]:
        sources_categories = cls._get_sources_categories()
        categories_news = defaultdict(int)
        for source, news_count in sources_news_count.items():
            if news_count:
                for category in sources_categories[source]:
                    categories_news[category] += news_count
        categories_news["all"] = sum(sources_news_count.values())
        return categories_news

    @classmethod
    def _new_news_messages_to_broker(cls, data: dict[int, int]) -> list[NewsMessage]:
        categories_news = cls._get_categories_news(data)
        return [
            NewsMessage(
                topic=category,
                value=news_count
            ) for category, news_count in categories_news.items()
        ]

    @classmethod
    def publish_updates(cls, data: dict[int, int]):
        messages = cls._new_news_messages_to_broker(data)
        publish_messages(messages)


class ElasticNews:
    @classmethod
    def _get_latest_indexed_news(cls) -> int:
        s = NewsDocument.search().sort("-id").query("match_all").extra(size=1)
        response = s.execute()
        if response.hits:
            return response.hits[0].id
        else:
            return 0

    @classmethod
    def sync_updates(cls):
        first_idx = cls._get_latest_indexed_news()
        actions = (
            {
                "_op_type": "index",
                "_index": NewsDocument.Index.name,
                "_id": obj.id,
                "_source": NewsDocument().prepare(obj)
            }
            for obj in News.objects.filter(id__gt=first_idx).iterator()
        )
        es = connections.get_connection()
        bulk(es, actions)

    @classmethod
    def update_registry(cls):
        registry.update(News)