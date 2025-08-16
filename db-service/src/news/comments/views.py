from rest_framework import generics, status, permissions
from rest_framework.response import Response

from .serializers import CommentModelSerializer, CommentCreateModelSerializer
from .models import Comment


class UsersCommentsByNewsPKAPIView(generics.ListAPIView):
    """Получить комментарии к новости"""
    queryset = Comment.objects.filter(active=True).select_related("user")
    serializer_class = CommentModelSerializer

    def list(self, request, *args, **kwargs):
        if not kwargs.get("pk"):
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "Не указан id новости"})
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.queryset.select_related("user").filter(news=self.kwargs["pk"])
        return queryset.only("body", "user", "user__username", "user__avatar", )


class CreateCommentByNewsPKAPIView(generics.CreateAPIView):
    """Добавить комментарий к новости"""
    queryset = Comment.objects.all()
    serializer_class = CommentCreateModelSerializer
    permission_classes = (permissions.IsAuthenticated,)
