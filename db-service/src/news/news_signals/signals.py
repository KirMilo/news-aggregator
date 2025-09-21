from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from news.models import News

from news.celery_tasks.tasks import publish_created_news, sync_news_index
from news.news_signals.custom_signals import news_created_signal



@receiver(signal=news_created_signal)
def on_create_news(**kwargs):  # noqa
    print("signal on create news")
    publish_created_news(kwargs["data"])
    sync_news_index()


@receiver(signal=post_save, sender=News)
def on_update_news(**kwargs):  # noqa
    print("signal on update news")
    # TODO логика отправки в брокер сообщения об обновлении новости и её категории и всех категорий
    print("kwargs: ", kwargs)
    sync_news_index()

@receiver(signal=post_delete, sender=News)
def on_delete_news(**kwargs):  # noqa
    print("signal on delete news")
    # TODO логика отправки в брокер сообщения об удалении новости
    sync_news_index()
