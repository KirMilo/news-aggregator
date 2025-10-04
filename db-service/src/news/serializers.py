from django_elasticsearch_dsl_drf_alt.serializers import DocumentSerializer
from rest_framework import serializers

from .models import News, NewsImage, Source, Category
from .documents import NewsDocument


class NewsDocumentSerializer(DocumentSerializer):
    class Meta:
        document = NewsDocument
        model = News
        fields = ("id", "title", "body", "published_at")
        read_only = True


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
            # "body",
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


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.to_representation(value)


class CategoriesModelSerializer(serializers.ModelSerializer):
    children = RecursiveField(many=True, allow_null=True, default=None)

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "slug",
            "children",
        )
