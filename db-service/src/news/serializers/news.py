from rest_framework import serializers

from .news_categories_mixin import NewsCategoriesMixin
from news.models import News

from news.utils.news_categories import fill_news_categories


class NewsByPKModelSerializer(serializers.ModelSerializer, NewsCategoriesMixin):
    # news_image = NewsImagesModelSerializer()

    class Meta:
        model = News
        fields = (
            "title",
            "body",
            "published_at",
            "categories",
        )

    def to_representation(self, instance):
        return fill_news_categories([instance])[0]


class NewsModelSerializer(serializers.ModelSerializer, NewsCategoriesMixin):
    class Meta:
        model = News
        fields = (
            "id",
            "title",
            "published_at",
            "categories",
        )
