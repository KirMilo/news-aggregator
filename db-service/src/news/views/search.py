from django_elasticsearch_dsl_drf_alt.viewsets import BaseDocumentViewSet
from django_elasticsearch_dsl_drf_alt.filter_backends import (
    CompoundSearchFilterBackend,
    OrderingFilterBackend, DefaultOrderingFilterBackend,
)
from drf_spectacular.utils import extend_schema

from news.documents import NewsDocument
from news.serializers import NewsDocumentSerializer, SearchNewsQuerySerializer


@extend_schema(tags=['Новости'], parameters=[SearchNewsQuerySerializer])
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
