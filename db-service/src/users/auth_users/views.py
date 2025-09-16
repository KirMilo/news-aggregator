from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.auth_users.serializers import RegistrationSerializer, UserLoginSerializer, UserLogoutSerializer


# https://habr.com/ru/articles/793058/

@extend_schema(request=RegistrationSerializer)
class RegistrationAPIView(APIView):  # RegisterUser
    def post(self, request):  # NOQA
        serializer = RegistrationSerializer(data=request.data)
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


# ConfirmRegisterUser

@extend_schema(request=UserLoginSerializer)
class LoginAPIView(APIView):
    # LoginUser
    def post(self, request):  # NOQA
        data = request.data

        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if (username or email) is None or password is None:
            return Response(
                {"error": "Provide username or email and password"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if username:
            user = authenticate(
                username=username,
                password=password
            )
        else:
            user = authenticate(
                email=email,
                password=password,
            )

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

@extend_schema(request=UserLogoutSerializer)
class LogoutAPIView(APIView):  # LogoutUser
    def post(self, request):  # NOQA
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return Response(
                {"error": "Provide refresh token"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()

        except Exception as e:
            return Response(
                {"error": "Invalid token"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"success": "Logged out"},
            status=status.HTTP_200_OK,
        )

# TODO: Сделать # UserPasswordChange
