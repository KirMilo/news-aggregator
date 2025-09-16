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
    class Meta:
        model = Comment
        fields = ("id", "body", "published_at")


class UserCommentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True, source="user__id")
    username = serializers.CharField(read_only=True, source="user__username")
    avatar = serializers.URLField(read_only=True, source="user__avatar", allow_blank=True)

    class Meta:
        model = get_user_model()
        fields = ("id", "username", "avatar",)


class CommentResponseSerializer(serializers.Serializer):
    user = UserCommentSerializer(source="*")
    comment = CommentModelSerializer(source="*")


class CurrentNewsPk:
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context["request"].parser_context["kwargs"]["pk"]


class CommentCreateModelSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    news_id = serializers.HiddenField(default=CurrentNewsPk())

    class Meta:
        model = Comment
        fields = (
            "news_id",
            "body",
            "user",
        )
