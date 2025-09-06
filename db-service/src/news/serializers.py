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
            "published_at"
        )
        extra_kwargs = {
            "published_at": {"read_only": False}
        }


class SourceDTModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = (
            "id",
            "updated_at",
        )
        extra_kwargs = {
            "id": {"read_only": False},
            "updated_at": {"read_only": False},
        }


class CreateNewsFieldsSerializer(serializers.Serializer):
    source = SourceDTModelSerializer()
    news = serializers.ListField(child=CreateNewsModelSerializer())


class CreateNewsSerializer(serializers.Serializer):
    data = serializers.ListField(child=CreateNewsFieldsSerializer())


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
