from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView as DefaultTokenRefreshView

from users.auth_users.serializers import (
    RegistrationSerializer,
    UserLoginSerializer,
    UserLogoutSerializer,
    SuccessLogoutSerializer,
)



@extend_schema(tags=['Авторизация'])
class TokenRefreshView(DefaultTokenRefreshView):
    pass


@extend_schema(tags=['Авторизация'])
class RegistrationAPIView(APIView):  # RegisterUser
    serializer_class = RegistrationSerializer

    @extend_schema(responses={201: TokenRefreshSerializer})
    def post(self, request):  # NOQA
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        refresh = RefreshToken.for_user(user)

        refresh.payload.update(
            {
                "user_id": user.id,
                "username": user.username,
            }
        )
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_201_CREATED,
        )


@extend_schema(tags=['Авторизация'])
class LoginAPIView(APIView):
    serializer_class = UserLoginSerializer

    @extend_schema(responses={200: TokenRefreshSerializer})
    def post(self, request):  # NOQA
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(**serializer.validated_data)
        if user is None:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        refresh = RefreshToken.for_user(user)
        refresh.payload.update(
            {
                "user_id": user.id,
                "username": user.username,
            }
        )

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_200_OK,
        )


@extend_schema(tags=['Авторизация'])
class LogoutAPIView(APIView):  # LogoutUser
    serializer_class = UserLogoutSerializer

    @extend_schema(responses={200: SuccessLogoutSerializer})
    def post(self, request) -> Response:  # NOQA
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh_token = serializer.validated_data['refresh_token']
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:  # NOQA
            return Response(
                {"error": "Invalid token"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"success": "Logged out"},
            status=status.HTTP_200_OK,
        )

# TODO: Сделать UserPasswordChange и ConfirmRegisterUser
