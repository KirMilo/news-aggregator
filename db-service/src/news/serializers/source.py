from rest_framework import serializers

from news.models import Source


class SourceModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = (
            "id",
            "link",
            "updated_at",
        )
