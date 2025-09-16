from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from users.auth_users.views import LoginAPIView, LogoutAPIView, RegistrationAPIView

urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegistrationAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
]
