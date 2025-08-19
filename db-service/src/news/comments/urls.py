from django.urls import path

from news.comments import views as comments_views


urlpatterns = [
    path('', comments_views.UsersCommentsByNewsPKAPIView.as_view()),
    path('create/', comments_views.CreateCommentByNewsPKAPIView.as_view()),
]
