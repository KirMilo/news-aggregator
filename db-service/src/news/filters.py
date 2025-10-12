from datetime import datetime

import django_filters

from news.serializers import NewsQuerySerializer
from news.serializers.query import FreshNewsQuerySerializer


class NewsFilterBase(django_filters.FilterSet):
    """Базовый класс фильтров новостей"""
    category = django_filters.CharFilter(
        label='Slug категории',
        field_name='category',
        method='filter_by_category',
    )
    offset = django_filters.DateTimeFilter()
    limit = django_filters.NumberFilter(
        label='Количество записей',
        method='set_limit',
        initial=10,
    )
    serializer_class = ...

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        query = self.serializer_class(data=self.data)
        query.is_valid(raise_exception=True)
        self.data = query.validated_data

    def filter_by_category(self, queryset, name, value):  # noqa
        if value:
            queryset = queryset.filter(categories__contains=[value])
        return queryset

    def set_limit(self, queryset, name, value):  # noqa
        limit = self.data["limit"]
        return queryset[:limit]


class NewsFilter(NewsFilterBase):
    serializer_class = NewsQuerySerializer
    offset = django_filters.DateTimeFilter(
        label='Прямой сдвиг по дате (lt)',
        method='set_offset',
    )

    def set_offset(self, queryset, name, value): # noqa
        if offset := self.data.get("offset"):
            queryset = queryset.filter(published_at__lt=offset)
        return queryset


class FreshNewsFilter(NewsFilterBase):
    serializer_class = FreshNewsQuerySerializer
    offset = django_filters.DateTimeFilter(
        label='Обратный сдвиг по дате (gt)',
        method='set_offset',
        required=True,
    )

    def set_offset(self, queryset, name, value): # noqa
        offset = self.data.get("offset") or datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        return queryset.filter(published_at__gt=offset)
