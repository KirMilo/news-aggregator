from rest_framework import serializers


class NewsQuerySerializer(serializers.Serializer):
    limit = serializers.IntegerField(default=10, min_value=1, max_value=100, required=False)
    offset = serializers.DateTimeField(required=False)
    category = serializers.CharField(max_length=100, required=False)


class FreshNewsQuerySerializer(NewsQuerySerializer):
    offset = serializers.DateTimeField(required=True)



class SearchNewsQuerySerializer(serializers.Serializer):
    search = serializers.CharField(max_length=100, required=False)
