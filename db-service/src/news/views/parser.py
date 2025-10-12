from typing import List, Dict, Any

from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.response import Response
from news.models import News, Source
from news.serializers import CreateNewsSerializer, SourceModelSerializer
from news.news_signals.custom_signals import news_created_signal


@extend_schema(tags=['Парсер'])
class NewsSourcesAPIView(generics.ListAPIView):
    """Получить список источников новостей"""
    serializer_class = SourceModelSerializer
    queryset = Source.objects.filter(active=True)
    pagination_class = None


@extend_schema(tags=['Парсер'])
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
