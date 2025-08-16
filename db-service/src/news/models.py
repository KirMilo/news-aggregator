
from django.db import models


class News(models.Model):  # Новости
    title = models.CharField(max_length=255)
    body = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)
    link = models.URLField()
    active = models.BooleanField(default=True)

    categories = models.ManyToManyField("NewsCategory", related_name='news_categories')
    source = models.ForeignKey("Source", on_delete=models.SET_NULL, related_name='news_sources', null=True)

    def __str__(self):
        return self.title


class Category(models.Model):  # Категории
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class NewsCategory(models.Model):  # Ассоциативная таблица новости-категории
    news_id = models.ForeignKey("News", on_delete=models.CASCADE, related_name='news_news_id')
    category = models.ForeignKey("Category", on_delete=models.SET_NULL, related_name='news_category_id', null=True)


class NewsImage(models.Model):  # Прикрепленные к новости изображения
    url = models.URLField()
    news = models.OneToOneField(News, on_delete=models.CASCADE, related_name='news_image')


class Source(models.Model):
    link = models.URLField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.link
