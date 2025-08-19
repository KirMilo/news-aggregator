
import itertools
from typing import Iterable, Generator

from rest_framework import generics, status
from django_elasticsearch_dsl_drf import viewsets as elastic_viewsets
from django_elasticsearch_dsl_drf.filter_backends import (
    CompoundSearchFilterBackend,
    OrderingFilterBackend,
)
from rest_framework.response import Response

from .models import News
from .documents import NewsDocument
from .pagination import NewsAPIListPagination
from .serializers import NewsModelSerializer, NewsDocumentSerializer, CreateNewsSerializer


class CreateNewsAPIView(generics.CreateAPIView):  # TODO: Это протестить
    """ViewSet для создания новостей в БД"""
    queryset = News.objects.all()
    serializer_class = CreateNewsSerializer

    @staticmethod
    def news_to_models(serializer_data: Iterable) -> itertools.chain:
        news: list[Generator] = []
        for item in serializer_data:
            source = item.source
            categories = item.categories
            news += (News(source=source, categories=categories, **news_items) for news_items in item.data)

        return itertools.chain(*news)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        news = self.news_to_models(serializer.validated_data)
        News.objects.bulk_create(news)
        headers = self.get_success_headers(serializer.data)
        return Response(status=status.HTTP_201_CREATED, headers=headers)


class FreshNewsAPIView(generics.ListAPIView):  # Тут вроде ок
    """Получить список свежих новостей по категории или без категории"""
    serializer_class = NewsModelSerializer
    pagination_class = NewsAPIListPagination

    def get_queryset(self):
        queryset = News.objects.all().order_by("-published_at")
        if category := self.request.query_params.get("category"):  # Noqa
            queryset = queryset.filter(category=category)
        return queryset


class NewsByPKAPIView(generics.RetrieveAPIView):  # Тут вроде ок
    """Получить новость по id"""
    serializer_class = NewsModelSerializer

    def get_queryset(self):
        queryset = News.objects.filter(pk=self.kwargs["pk"])
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
        "published_at": None,   # Слева - это название в Query, справа - это название в Документе.
        # None - это значит, что названия в Query и в Документе совпадают.
    }

    ordering = ("-published_at",)  # Указываем порядок сортировки по умолчанию

# get_category_list

