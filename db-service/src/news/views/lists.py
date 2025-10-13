from collections import defaultdict

from django.contrib.postgres.aggregates import ArrayAgg
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.response import Response
from django_filters import rest_framework as drf_filters

from news.filters import NewsFilter, FreshNewsFilter
from news.models import News, Category
from news.serializers import NewsModelSerializer, CategoriesModelSerializer
from news.utils.news_categories import fill_news_categories


NEWS_LIST_KEY_PREFIX = "GET_NEWS_LIST"


@extend_schema(tags=['Новости'])
class NewsAPIView(generics.ListAPIView):
    """Получить список новостей по категории или без категории"""
    serializer_class = NewsModelSerializer
    pagination_class = None
    filter_backends = (drf_filters.DjangoFilterBackend,)
    filterset_class = NewsFilter

    def get_queryset(self):  # NOQA
        return (
            News.objects
            .select_related("source")
            .prefetch_related("categories")
            .values("id", "title", "published_at")
            .annotate(categories=ArrayAgg("source__categories__slug"))
            .filter(active=True)
            .order_by("-published_at")
        )

    def filter_queryset(self, queryset):
        filterset = self.filterset_class(self.request.query_params, queryset=queryset)  # NOQA
        return filterset.qs

    def list(self, request, *args, **kwargs):
        queryset = fill_news_categories(self.filter_queryset(self.get_queryset()))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @method_decorator(cache_page(60 * 3, key_prefix=NEWS_LIST_KEY_PREFIX))
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)


@extend_schema(tags=['Новости'])
class FreshNewsAPIView(generics.ListAPIView):
    """Получить список свежих новостей по категории или без категории"""
    serializer_class = NewsModelSerializer
    pagination_class = None
    filter_backends = (drf_filters.DjangoFilterBackend,)
    filterset_class = FreshNewsFilter

    def get_queryset(self):  # NOQA
        return (
            News.objects
            .select_related("source")
            .prefetch_related("categories")
            .values("id", "title", "published_at")
            .annotate(categories=ArrayAgg("source__categories__slug"))
            .filter(active=True)
            .order_by("published_at")
        )

    def filter_queryset(self, queryset):
        filterset = self.filterset_class(self.request.query_params, queryset=queryset)  # NOQA
        return filterset.qs

    def list(self, request, *args, **kwargs):
        queryset = fill_news_categories(self.filter_queryset(self.get_queryset()))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data[::-1])

    @method_decorator(cache_page(60 * 3))
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)


@extend_schema(tags=['Новости'])
class NewsCategoriesAPIView(generics.ListAPIView):
    """Получить список категорий новостей"""
    serializer_class = CategoriesModelSerializer
    queryset = Category.objects.all()
    pagination_class = None

    def list(self, request, *args, **kwargs):
        cats = self.filter_queryset(self.get_queryset())
        parents = defaultdict(list)
        for category in filter(lambda cat: cat.parent_id is not None, cats):
            parents[category.parent_id].append(category)
        for category in cats:
            category.children = parents[category.id]
        serializer = self.get_serializer([cat for cat in cats if cat.parent_id is None], many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
