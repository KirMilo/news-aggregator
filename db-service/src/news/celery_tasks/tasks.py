from news.celery_tasks.utils import ElasticNews, RabbitMQNews


# @celery_app.task
def sync_news_index():
    """Подтягивает последние созданные новости из БД в индекс Elasticsearch"""
    ElasticNews.sync_updates()


# @celery_app.task
def update_news_index():
    """Обновляет индекс Elasticsearch, если записи были изменены"""
    ElasticNews.update_registry()


# @celery_app.task
def publish_created_news(data: dict[int, int]):
    """Отправляет информацию об обновлениях в RabbitMQ"""
    RabbitMQNews.publish_updates(data)
