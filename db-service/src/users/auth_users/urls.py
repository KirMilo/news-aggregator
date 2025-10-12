from django.urls import path


from users.auth_users import views


urlpatterns = [
    path('token/refresh/', views.TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.RegistrationAPIView.as_view(), name='register'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('logout/', views.LogoutAPIView.as_view(), name='logout'),
]
