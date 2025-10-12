from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserProfileSerializer(serializers.ModelSerializer):
    # _private_fields = ("email",)
    is_owner = serializers.BooleanField()

    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "avatar",
            "date_joined",
            "is_owner",
        )
        extra_kwargs = {"date_joined": {"read_only": True}}

    def to_representation(self, instance):
        request = self.context.get("request", None)
        is_owner = (request and request.user and request.user.is_authenticated and request.user == self.instance)
        instance.is_owner = is_owner
        return super().to_representation(instance)


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "avatar",
        )


class IsAuthenticatedUserSerializer(serializers.Serializer):
    user = serializers.IntegerField()

