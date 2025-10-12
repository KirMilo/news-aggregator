from django_elasticsearch_dsl_drf_alt.serializers import DocumentSerializer
from news.documents import NewsDocument
from news.models import News
from .news_categories_mixin import NewsCategoriesMixin


class NewsDocumentSerializer(DocumentSerializer, NewsCategoriesMixin):
    class Meta:
        document = NewsDocument
        model = News
        fields = ("id", "title", "published_at", "categories")
        read_only = True
