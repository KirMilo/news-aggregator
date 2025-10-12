from rest_framework import serializers

from news.models import NewsImage


class NewsImagesModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsImage
        fields = ("url",)
