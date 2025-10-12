from django.contrib.postgres.aggregates import ArrayAgg
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_spectacular.utils import extend_schema
from rest_framework import generics

from news.models import News
from news.serializers import NewsByPKModelSerializer


@extend_schema(tags=['Новости'])
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