from rest_framework import serializers

from news.models import Category


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
