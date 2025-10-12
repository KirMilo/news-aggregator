from drf_spectacular.utils import extend_schema
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.db.utils import IntegrityError

from .serializers import CommentResponseSerializer, CommentCreateModelSerializer
from .models import Comment


@extend_schema(tags=['Комментарии'])
class UsersCommentsByNewsPKAPIView(generics.ListAPIView):
    """Получить комментарии к новости"""
    serializer_class = CommentResponseSerializer

    def get_queryset(self):
        queryset = (
            Comment.objects.filter(active=True)
            .select_related("user")
            .filter(news=self.kwargs["pk"])
            .values("id", "body", "published_at", "user__id", "user__username", "user__avatar", )
        )
        return queryset


@extend_schema(tags=['Комментарии'])
class CreateCommentByNewsPKAPIView(generics.CreateAPIView):
    """Добавить комментарий к новости"""
    serializer_class = CommentCreateModelSerializer
    permission_classes = (permissions.IsAuthenticated,) # (permissions.IsAuthenticatedOrReadOnly,)

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"detail": f"News id '{kwargs["news"]}' not found"},
            )
