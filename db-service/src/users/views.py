from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    UserProfileSerializer,
    UserUpdateSerializer,
    IsAuthenticatedUserSerializer,
)


@extend_schema(tags=['Пользователь'])
class UserProfileView(generics.RetrieveAPIView):
    """Профиль пользователя по его id"""
    serializer_class = UserProfileSerializer
    queryset = get_user_model().objects.all()


@extend_schema(tags=['Пользователь'])
class UserUpdateView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserUpdateSerializer
    http_method_names = ["patch", "options", "head", ]

    def get_object(self):
        return self.request.user


@extend_schema(tags=['Пользователь'])
class IsAuthenticatedView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = IsAuthenticatedUserSerializer

    def get(self, request):  # NOQA
        return Response(
            {"user": request.user.id},
            status=status.HTTP_200_OK,
        )