from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Comment


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "username",
            "avatar",
        )


class CommentModelSerializer(serializers.ModelSerializer):
    user = UserModelSerializer()

    class Meta:
        model = Comment
        fields = ("body", "published_at", "user", )


class CommentCreateModelSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Comment
        fields = ("news_id", "body", "user",)  # TODO: Прочекать работу
