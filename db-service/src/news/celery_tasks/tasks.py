from core import celery_app
from news.celery_tasks.utils import ElasticNews, RabbitMQNews


@celery_app.task
def sync_news_index():
    """Подтягивает последние созданные новости из БД в индекс Elasticsearch"""
    ElasticNews.sync_updates()


@celery_app.task
def publish_created_news(*args, **kwargs):
    """Отправляет информацию об обновлениях в RabbitMQ"""
    RabbitMQNews.publish_created_news(*args, **kwargs)


@celery_app.task
def publish_updated_news(*args, **kwargs):
    """Отправляет информацию об обновлении новости в RabbitMQ"""
    RabbitMQNews.publish_updated_news(*args, **kwargs)


@celery_app.task
def publish_deleted_news(*args, **kwargs):
    """Отправляет информацию об удалении новости в RabbitMQ"""
    RabbitMQNews.publish_deleted_news(*args, **kwargs)
