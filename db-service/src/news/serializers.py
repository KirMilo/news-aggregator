from rest_framework import serializers

from .models import News, Category, NewsImage, Source
from .documents import NewsDocument


class NewsDocumentSerializer(serializers.Serializer):
    class Meta:
        document = NewsDocument
        fields = "__all__"


class CategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
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
    categories = serializers.ListField(child=serializers.IntegerField())
    data = serializers.ListField(child=CreateNewsModelSerializer())


class NewsModelSerializer(serializers.ModelSerializer):
    categories = serializers.ListField(child=serializers.IntegerField())
    news_image = NewsImagesModelSerializer()

    class Meta:
        model = News
        fields = ("title", "body", "published_at", "news_image", "categories",)
