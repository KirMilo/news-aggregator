from django.contrib.auth import get_user_model
from django.db import models


class Comment(models.Model):
    body = models.TextField(max_length=255)
    active = models.BooleanField(default=True)
    published_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='comments', null=True)
    news = models.ForeignKey("news.News", on_delete=models.CASCADE, related_name='comments', null=True)
