from django.db import migrations
from news.models import Source, Category


def create_self_source(*args, **kwargs):  # NOQA
    categories = Category.objects.all()
    source = Source(
        link="https://news-aggregator/",
        active=False,
    )
    source.save()
    source.categories.set(list(categories))


class Migration(migrations.Migration):
    dependencies = [
        ('news', '0006_alter_news_published_at'),
    ]

    operations = [
        migrations.RunPython(
            create_self_source,
        ),
    ]
