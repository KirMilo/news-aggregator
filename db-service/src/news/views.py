
import itertools
from typing import Iterable, Generator

from rest_framework import generics, status
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    CompoundSearchFilterBackend,
    OrderingFilterBackend,
)
from rest_framework.response import Response

from .models import News
from .documents import NewsDocument
from .pagination import NewsAPIListPagination
from .serializers import NewsModelSerializer, NewsDocumentSerializer, CreateNewsSerializer


class CreateNewsAPIView(generics.CreateAPIView):
    """ViewSet для создания новостей в БД"""
    queryset = News.objects.all()
    serializer_class = CreateNewsSerializer

    @staticmethod
    def news_models(serializer_data: Iterable) -> itertools.chain:
        news: list[Generator] = []
        for item in serializer_data:
            source = item.source
            categories = item.categories
            news += (News(source=source, categories=categories, **news_items) for news_items in item.data)

        return itertools.chain(*news)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        news = self.news_models(serializer.validated_data)  # или .data
        News.objects.bulk_create(news)
        headers = self.get_success_headers(serializer.data)
        return Response(status=status.HTTP_201_CREATED, headers=headers)


class FreshNewsAPIView(generics.ListAPIView):
    """Получить список свежих новостей по категории или без категории"""
    queryset = News.objects.all().order_by("-published_at")
    serializer_class = NewsModelSerializer
    pagination_class = NewsAPIListPagination

    def get_queryset(self):
        queryset = self.queryset
        if category := self.kwargs.get("category"):
            queryset = queryset.filter(category=category)
        return queryset


class NewsByPKAPIView(generics.RetrieveAPIView):
    """Получить новость по id"""
    queryset = News.objects.all()
    serializer_class = NewsModelSerializer


class NewsDocumentView(DocumentViewSet):
    """ViewSet для получения новостей из Elasticsearch"""  # Ручка для поиска новостей через Elasticsearch
    document = NewsDocument
    serializer_class = NewsDocumentSerializer

    filter_backends = (  # TODO: Чекнуть доку
        FilteringFilterBackend,
        CompoundSearchFilterBackend,
        OrderingFilterBackend,
    )
    search_fields = ("title", "body",)  # TODO: Чекнуть доку
    filter_fields = {
        "id": "id",
        "time_created": "time_created",
    }
    ordering_fields = {
        "id": None,
        "title": "title.keyword",
    }


# get_category_list

