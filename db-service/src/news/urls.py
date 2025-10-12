from django.urls import path, include

from .comments.urls import urlpatterns as comments_patterns
from news import views as news_views

urlpatterns = [
    path('', news_views.NewsAPIView.as_view()),
    path('fresh', news_views.FreshNewsAPIView.as_view()),
    path('<int:pk>/', news_views.NewsByPKAPIView.as_view()),
    path('search', news_views.NewsSearchDocumentViewSet.as_view({"get": "list"})),
    path('create/', news_views.CreateNewsAPIView.as_view()),
    path('categories/', news_views.NewsCategoriesAPIView.as_view()),
    path('sources/', news_views.NewsSourcesAPIView.as_view()),
    path('<int:pk>/comments/', include(comments_patterns)),
]
