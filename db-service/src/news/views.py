from typing import List, Dict, Any

from django.contrib.postgres.aggregates import ArrayAgg
from rest_framework import generics, status
from django_elasticsearch_dsl_drf import viewsets as elastic_viewsets
from django_elasticsearch_dsl_drf.filter_backends import (
    CompoundSearchFilterBackend,
    OrderingFilterBackend,
)
from rest_framework.response import Response

from .models import News, Source
from .documents import NewsDocument
from .pagination import NewsAPIListPagination
from .serializers import (
    NewsModelSerializer,
    NewsDocumentSerializer,
    CreateNewsSerializer,
    SourceModelSerializer,
    NewsByPKModelSerializer,
)


class NewsSourcesAPIView(generics.ListAPIView):  # Тут ок
    """Получить список источников новостей"""
    serializer_class = SourceModelSerializer
    queryset = Source.objects.filter(active=True)
    pagination_class = None


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


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.sources_news_create(serializer.validated_data["data"])
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
            .values("id", "title", "body", "published_at")
            .annotate(categories=ArrayAgg("source__categories__name"))
            .filter(active=True)
            .order_by("-published_at")
        )
        if category := self.request.query_params.get("category"):  # NOQA
            queryset = queryset.filter(categories__contains=[category])

        return queryset


class NewsByPKAPIView(generics.RetrieveAPIView):
    """Получить новость по id"""
    serializer_class = NewsByPKModelSerializer

    def get_queryset(self):
        queryset = (
            News.objects
            .select_related("source")
            .prefetch_related("categories")
            .values("id", "title", "body", "published_at")
            .annotate(categories=ArrayAgg("source__categories__name"))
            .filter(pk=self.kwargs["pk"]))
        return queryset


class NewsSearchDocumentViewSet(elastic_viewsets.DocumentViewSet):  # TODO: Это протестить
    """ViewSet для получения новостей из Elasticsearch"""  # Ручка для поиска новостей через Elasticsearch
    document = NewsDocument
    serializer_class = NewsDocumentSerializer

    filter_backends = (  # Это фильтры, которые будут применяться к запросу
        # FilteringFilterBackend, # Точная фильтрация по конкретным полям
        CompoundSearchFilterBackend,  # Поиск по нескольким полям, определенным в search_fields
        OrderingFilterBackend,  # Сортировка результатов по полям
    )

    search_fields = ("title", "body",)  # Определяем поля для полнотекстового поиска

    ordering_fields = {  # Указываем поля для упорядочивания
        "published_at": None,  # Слева - это название в Query, справа - это название в Документе.
        # None - это значит, что названия в Query и в Документе совпадают.
    }

    ordering = ("-published_at",)  # Указываем порядок сортировки по умолчанию
