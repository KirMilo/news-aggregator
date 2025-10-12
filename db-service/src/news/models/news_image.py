from django.db import models

class NewsImage(models.Model):
    """Изображения новостей (Не используются на данный момент)"""
    url = models.URLField()

    news = models.OneToOneField("News", on_delete=models.CASCADE, related_name='news_image')
