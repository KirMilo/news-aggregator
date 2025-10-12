from django.urls import path

from users.views import UserProfileView, IsAuthenticatedView, UserUpdateView

urlpatterns = [
    path('authenticated/', IsAuthenticatedView.as_view()),
    path('<int:pk>/', UserProfileView.as_view()),
    path('', UserUpdateView.as_view()),
]
