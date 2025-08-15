from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import CommentModelSerializer
from .models import Comment


class UsersCommentsByNewsPKAPIView(generics.ListAPIView):
    """Получить комментарии к новости"""
    queryset = Comment.objects.filter(active=True)
    serializer_class = CommentModelSerializer

    def list(self, request, *args, **kwargs):
        if not (news_pk := kwargs.get("pk")):
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "Не указан id новости"})

        queryset = self.get_queryset().select_related("user").filter(news=news_pk).join()
