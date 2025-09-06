from rest_framework import serializers

from .models import News, NewsImage, Source
from .documents import NewsDocument


class NewsDocumentSerializer(serializers.Serializer):
    class Meta:
        document = NewsDocument
        fields = "__all__"


class NewsImagesModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsImage
        fields = ("url",)


class CreateNewsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = (
            "title",
            "body",
            "link",
        )


class CreateNewsSerializer(serializers.Serializer):
    source = serializers.IntegerField()
    data = serializers.ListField(child=CreateNewsModelSerializer())


class NewsByPKModelSerializer(serializers.ModelSerializer):
    categories = serializers.ListField(child=serializers.CharField())
    # news_image = NewsImagesModelSerializer()

    class Meta:
        model = News
        fields = (
            "title",
            "body",
            "published_at",
            "categories",
        )


class NewsModelSerializer(NewsByPKModelSerializer):
    class Meta:
        model = News
        fields = (
            "id",
            "title",
            "body",
            "published_at",
            "categories",
        )


class SourceModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = (
            "id",
            "link",
            "updated_at",
        )
