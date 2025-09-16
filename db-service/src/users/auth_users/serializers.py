from django.contrib.auth import get_user_model
from rest_framework import serializers


class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    password2 = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = get_user_model()
        fields = (
            'email',
            "username",
            "password",
            "password2",
        )

    def validate(self, data):
        if data.get('password') != data.get('password2'):
            raise serializers.ValidationError({"Passwords don't match"})
        data.pop('password2')
        return super().validate(data)


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(default=None)
    email = serializers.EmailField(default=None)
    password = serializers.CharField()


class UserLogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True)
