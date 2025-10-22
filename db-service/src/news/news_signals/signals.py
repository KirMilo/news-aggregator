from django.db.models.signals import post_save, pre_delete, post_delete
from django.dispatch import receiver
from django_elasticsearch_dsl.registries import registry
from django.core.cache import cache

from news.models import News

from news.celery_tasks.tasks import (
    publish_created_news,
    sync_news_index,
    publish_updated_news,
    publish_deleted_news,
)
from news.news_signals.custom_signals import news_created_signal
from news.views.lists import NEWS_LIST_KEY_PREFIX


@receiver(signal=news_created_signal)
def on_create_news(**kwargs):
    cache.delete_many(cache.keys("*" + NEWS_LIST_KEY_PREFIX + "*"))  # NOQA
    publish_created_news.delay(kwargs["data"])
    sync_news_index.delay()



@receiver(signal=post_save, sender=News)
def on_update_news(**kwargs):
    if kwargs["created"]:
        data = {kwargs["instance"].source.id: 1}
        publish_created_news.delay(data)
    elif kwargs["instance"].active:
        publish_updated_news.delay(kwargs["instance"].id)
    else:
        publish_deleted_news.delay(kwargs["instance"].id)
    registry.update(kwargs["instance"])
    cache.delete_many(cache.keys("*" + NEWS_LIST_KEY_PREFIX + "*"))  # NOQA


@receiver(signal=pre_delete, sender=News)
def pre_delete_news(**kwargs):
    cache.delete_many(cache.keys("*" + NEWS_LIST_KEY_PREFIX + "*"))  # NOQA
    publish_deleted_news(kwargs["instance"].id)  # Тут без .delay()


@receiver(signal=post_delete, sender=News)
def post_delete_news(**kwargs):  # noqa
    registry.update(kwargs["instance"])

