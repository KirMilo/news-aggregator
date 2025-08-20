from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.db.utils import IntegrityError

from .serializers import CommentModelSerializer, CommentCreateModelSerializer
from .models import Comment


class UsersCommentsByNewsPKAPIView(generics.ListAPIView):
    """Получить комментарии к новости"""
    queryset = Comment.objects.filter(active=True).select_related("user")
    serializer_class = CommentModelSerializer

    def get_queryset(self):
        queryset = self.queryset.filter(news=self.kwargs["news"])
        return queryset.only("body", "user", "user__username", "user__avatar", )


class CreateCommentByNewsPKAPIView(generics.CreateAPIView):
    """Добавить комментарий к новости"""
    serializer_class = CommentCreateModelSerializer
    # permission_classes = (permissions.IsAuthenticated,) (permissions.IsAuthenticatedOrReadOnly,)

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError:
            return Response(
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                data={"detail": f"News id '{kwargs["news"]}' not found"},
            )
