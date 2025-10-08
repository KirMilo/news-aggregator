from cache_memoize import cache_memoize

from news.models import Category


@cache_memoize(60 * 15)
def get_categories() -> dict[str, dict[str, str | int]]:
    cats = {}
    for cat in Category.objects.values("id", "name", "slug").all():
        cats[cat["slug"]] = {
            "id": cat["id"],
            "name": cat["name"],
            "slug": cat["slug"],
        }
    return cats


def fill_news_categories[T](queryset: T) -> T:
    cats = get_categories()
    for item in queryset:
        item["categories"] = [cats[cat] for cat in item["categories"]]
    return queryset
