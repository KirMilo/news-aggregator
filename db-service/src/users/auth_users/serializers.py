from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework import serializers


class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, min_length=2)
    password = serializers.CharField(required=True, min_length=3, write_only=True)
    password2 = serializers.CharField(required=True, min_length=3, write_only=True)
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
        if get_user_model().objects.filter(email=str(data.get('email'))):
            raise serializers.ValidationError({'detail': 'A user with that email already exists.'})
        elif get_user_model().objects.filter(username=data.get('username')):
            raise serializers.ValidationError({'detail': 'A user with that username already exists.'})

        if data.get('password') != data.get('password2'):
            raise serializers.ValidationError({"detail": "Passwords don't match."})
        data.pop('password2')

        return super().validate(data)

    def create(self, validated_data):
        user = get_user_model()(**validated_data)
        user.set_password(validated_data.get('password'))
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(default=None)
    email = serializers.EmailField(default=None)
    password = serializers.CharField()


class UserLogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True)
