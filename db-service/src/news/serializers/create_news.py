from rest_framework import serializers
from news.models import News, Source


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


class CreateNewsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = (
            "title",
            "body",
            "link",
            "published_at"
        )


class CreateNewsFieldsSerializer(serializers.Serializer):
    source = SourceDTModelSerializer()
    news = serializers.ListField(child=CreateNewsModelSerializer())


class CreateNewsSerializer(serializers.Serializer):
    data = serializers.ListField(child=CreateNewsFieldsSerializer())
