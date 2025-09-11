from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django_elasticsearch_dsl.registries import registry
from news.models import News


@receiver(signal=(post_save, post_delete), sender=News)
def on_update_document(**kwargs):  # noqa
    registry.update(News)
