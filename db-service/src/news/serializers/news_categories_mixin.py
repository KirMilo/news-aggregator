from rest_framework import serializers

from news.models import Category


class NewsCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "slug")


class NewsCategoriesMixin(serializers.Serializer):
    categories = serializers.ListField(child=NewsCategoriesSerializer())
