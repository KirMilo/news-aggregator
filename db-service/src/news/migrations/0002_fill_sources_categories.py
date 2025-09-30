from django.db import migrations
from news.models import Source, Category


def create_sources_and_categories(*args, **kwargs):  # NOQA
    categories = [
        Category(
            name="Спорт",
            slug="sport",
        ),
        Category(
            name="Просто спорт",
            slug="just-sport"
        ),
        Category(
            name="Киберспорт",
            slug="cybersport"
        ),
        Category(
            name="Автоспорт",
            slug="autosport",
        ),
        Category(
            name="Политика",
            slug="politics",
        ),
        Category(
            name="Экономика и финансы",
            slug="economics-and-finances",
        ),
        Category(
            name="Экономика",
            slug="economics",
        ),
        Category(
            name="Финансы",
            slug="finances",
        ),
        Category(
            name="Наука и технологии",
            slug="science-and-technologies",
        ),
        Category(
            name="Наука",
            slug="science",
        ),
        Category(
            name="Технологии",
            slug="technologies",
        )
    ]
    Category.objects.bulk_create(categories)
    categories_map = {category.name: category for category in categories}
    categories_map["Просто спорт"].parent = categories_map["Спорт"]
    categories_map["Автоспорт"].parent = categories_map["Спорт"]
    categories_map["Киберспорт"].parent = categories_map["Спорт"]
    categories_map["Экономика"].parent = categories_map["Экономика и финансы"]
    categories_map["Финансы"].parent = categories_map["Экономика и финансы"]
    categories_map["Наука"].parent = categories_map["Наука и технологии"]
    categories_map["Технологии"].parent = categories_map["Наука и технологии"]

    for cat in categories_map.values():
        cat.save()

    sources = [
        (
            Source(
                link="https://www.championat.com/news/auto/1.html",
            ),
            [categories_map["Спорт"], categories_map["Автоспорт"]],
        ),
        (
            Source(
                link="https://www.cybersport.ru/tags/cs2",
            ),
            [categories_map["Спорт"], categories_map["Киберспорт"]],
        ),
        (
            Source(
                link="https://www.cybersport.ru/tags/dota-2",
            ),
            [categories_map["Спорт"], categories_map["Киберспорт"]],
        ),
        (
            Source(
                link="https://sportrbc.ru/",
            ),
            [categories_map["Спорт"], categories_map["Просто спорт"]],
        ),
        (
            Source(
                link="https://www.rbc.ru/technology_and_media/",
            ),
            [categories_map["Наука и технологии"]],
        ),
        (
            Source(
                link="https://www.rbc.ru/finances/",
            ),
            [categories_map["Экономика и финансы"], categories_map["Финансы"]],
        ),
        (
            Source(
                link="https://www.rbc.ru/economics/"
            ),
            [categories_map["Экономика и финансы"], categories_map["Экономика"]],
        ),
        (
            Source(
                link="https://www.rbc.ru/politics/", ),
            [categories_map["Политика"]],
        ),
        (
            Source(
                link="https://lenta.ru/rubrics/science/cosmos/", ),
            [categories_map["Наука и технологии"]],
        ),
        (
            Source(
                link="https://lenta.ru/rubrics/science/future/",
            ),
            [categories_map["Наука и технологии"]],
        ),
        (
            Source(
                link="https://lenta.ru/rubrics/science/science/",
            ),
            [categories_map["Наука и технологии"], categories_map["Наука"]],
        ),
        (
            Source(
                link="https://lenta.ru/rubrics/science/digital/",
            ),
            [categories_map["Наука и технологии"], categories_map["Технологии"]],
        ),
        (
            Source(  # Сам агрегатор
                link="https://news-aggregator/",
                active=False,
            ),
            list(categories_map.values()),
        )
    ]

    for source, categories in sources:
        source.save()
        source.categories.set(categories)


class Migration(migrations.Migration):
    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            create_sources_and_categories
        ),
    ]
