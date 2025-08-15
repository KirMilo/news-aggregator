from rest_framework import serializers

from .models import News, Category, NewsImages, Source
from .documents import NewsDocument


class NewsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = "__all__"


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
        model = NewsImages
        fields = "__all__"


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
