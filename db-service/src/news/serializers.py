from django_elasticsearch_dsl_drf_alt.serializers import DocumentSerializer
from rest_framework import serializers

from .models import News, NewsImage, Source, Category
from .documents import NewsDocument
from .utils.news_categories import fill_news_categories


class NewsCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "slug")


class NewsCategoriesMixin(serializers.Serializer):
    categories = serializers.ListField(child=NewsCategoriesSerializer())


class NewsDocumentSerializer(DocumentSerializer):
    class Meta:
        document = NewsDocument
        model = News
        fields = ("id", "title", "published_at", "categories")
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
