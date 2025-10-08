from collections import defaultdict
from typing import List, Dict, Any

from django.contrib.postgres.aggregates import ArrayAgg
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework import generics, status
from django_elasticsearch_dsl_drf_alt.viewsets import BaseDocumentViewSet
from django_elasticsearch_dsl_drf_alt.filter_backends import (
    CompoundSearchFilterBackend,
    OrderingFilterBackend, DefaultOrderingFilterBackend,
)
from rest_framework.response import Response

from .models import News, Source, Category
from .documents import NewsDocument
from .pagination import NewsAPIListPagination
from .serializers import (
    NewsModelSerializer,
    NewsDocumentSerializer,
    CreateNewsSerializer,
    SourceModelSerializer,
    NewsByPKModelSerializer,
    CategoriesModelSerializer,
)
from .news_signals.custom_signals import news_created_signal
from .utils.news_categories import fill_news_categories


class NewsSourcesAPIView(generics.ListAPIView):  # Тут ок
    """Получить список источников новостей"""
    serializer_class = SourceModelSerializer
    queryset = Source.objects.filter(active=True)
    pagination_class = None


class NewsCategoriesAPIView(generics.ListAPIView):
    """Получить список категорий новостей"""
    serializer_class = CategoriesModelSerializer
    queryset = Category.objects.all()

    def list(self, request, *args, **kwargs):
        cats = self.filter_queryset(self.get_queryset())
        parents = defaultdict(list)
        for category in filter(lambda cat: cat.parent_id is not None, cats):
            parents[category.parent_id].append(category)
        for category in cats:
            category.children = parents[category.id]
        serializer = self.get_serializer([cat for cat in cats if cat.parent_id is None], many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateNewsAPIView(generics.CreateAPIView):
    """ViewSet для создания новостей в БД"""
    serializer_class = CreateNewsSerializer

    @staticmethod
    def sources_news_create(serializer_data: List[Dict[str, Any]]):
        for item in serializer_data:
            source = Source.objects.get(pk=item["source"]["id"])
            source.updated_at = item["source"]["updated_at"]
            source.save()
            News.objects.bulk_create(News(source=source, **news_items) for news_items in item["news"])

    def send_signal_on_create(self, serializer_data: List[Dict[str, Any]]):
        sources_news = {item["source"]["id"]: len(item["news"]) for item in serializer_data}
        news_created_signal.send(sender=self.__class__.__name__, data=sources_news)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.sources_news_create(serializer.validated_data["data"])
        self.send_signal_on_create(serializer.validated_data["data"])
        headers = self.get_success_headers(serializer.data)
        return Response(status=status.HTTP_201_CREATED, headers=headers)


class FreshNewsAPIView(generics.ListAPIView):
    """Получить список свежих новостей по категории или без категории"""
    serializer_class = NewsModelSerializer
    pagination_class = NewsAPIListPagination

    def get_queryset(self):
        queryset = (
            News.objects
            .select_related("source")
            .prefetch_related("categories")
            .values("id", "title", "published_at")
            .annotate(
                categories=ArrayAgg("source__categories__slug"),
            )
            .filter(active=True)
            .order_by("-published_at")
        )
        if category := self.request.query_params.get("category"):  # NOQA
            queryset = queryset.filter(categories__contains=[category])

        return fill_news_categories(queryset)

    @method_decorator(cache_page(60 * 3))
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)


class NewsByPKAPIView(generics.RetrieveAPIView):
    """Получить новость по id"""
    serializer_class = NewsByPKModelSerializer

    def get_queryset(self):
        queryset = (
            News.objects
            .select_related("source")
            .prefetch_related("categories")
            .values(
                "id",
                "title",
                "body",
                "published_at",
            )
            .annotate(categories=ArrayAgg("source__categories__slug"))
            .filter(pk=self.kwargs["pk"]))
        return queryset

    @method_decorator(cache_page(60 * 3))
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)


class NewsSearchDocumentViewSet(BaseDocumentViewSet):
    """ViewSet для получения новостей из Elasticsearch"""  # Ручка для поиска новостей через Elasticsearch
    document = NewsDocument
    serializer_class = NewsDocumentSerializer

    filter_backends = (  # Это фильтры, которые будут применяться к запросу
        # FilteringFilterBackend, # Точная фильтрация по конкретным полям
        OrderingFilterBackend,  # Сортировка результатов по полям
        DefaultOrderingFilterBackend,  # Сортировка по умолчанию
        CompoundSearchFilterBackend,  # Поиск по нескольким полям, определенным в search_fields
    )

    search_fields = {
        "title": {"fuzziness": "AUTO", "boost": 3},
        "body": {"fuzziness": "AUTO", "boost": 1},
    }  # Определяем поля для полнотекстового поиска

    ordering_fields = {  # Указываем поля для упорядочивания
        "published_at": None,  # Слева - это название в Query, справа - это название в Документе.
        # None - совпадают.
    }

    ordering = ("_score", "-published_at",)  # Указываем порядок сортировки по умолчанию # _score - релевантность

    def get_queryset(self):
        queryset = self.search.query(
            "term",
            active=True,
        )  # Добавляем фильтрацию по active
        queryset.model = self.document.Django.model
        return queryset
