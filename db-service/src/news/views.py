from rest_framework import generics
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


class CreateNewsAPIView(generics.CreateAPIView):  # TODO: Скорее всего не получится сделать через ViewSet
    """ViewSet для создания новостей в БД"""  # Ручка для записи новостей в БД
    queryset = News.objects.all()
    serializer_class = CreateNewsSerializer


class NewsDocumentView(DocumentViewSet):
    """ViewSet для получения новостей из Elasticsearch"""  # Ручка для поиска новостей через Elasticsearch
    document = NewsDocument
    serializer_class = NewsDocumentSerializer

    filter_backends = ( # TODO: Чекнуть доку
        FilteringFilterBackend,
        CompoundSearchFilterBackend,
        OrderingFilterBackend,
    )
    search_fields = ("title", "body",) # TODO: Чекнуть доку
    filter_fields = {
        "id": "id",
        "time_created": "time_created",
    }
    ordering_fields = {
        "id": None,
        "title": "title.keyword",
    }


class FreshNewsAPIView(generics.ListAPIView):
    """Получить список свежих новостей по категории или без категории"""
    queryset = News.objects.all().order_by("-published_at")
    serializer_class = NewsModelSerializer
    pagination_class = NewsAPIListPagination

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if category := kwargs.get("category"):
            queryset = queryset.filter(category=category)

        queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class NewsByPKAPIView(generics.RetrieveAPIView):
    """Получить новость по id"""
    queryset = News.objects.all()
    serializer_class = NewsModelSerializer

    """
    {
        "source": 1,
        "categories": [1, 2]
        "data": [
            
        ]
    }
    """
