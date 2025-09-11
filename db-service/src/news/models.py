from django.db import models


class News(models.Model):  # Новости
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    body = models.TextField(verbose_name="Статья")
    published_at = models.DateTimeField(verbose_name="Дата публикации")
    link = models.URLField(verbose_name="Ссылка")
    active = models.BooleanField(default=True, verbose_name="Опубликовано")

    source = models.ForeignKey(
        "Source",
        on_delete=models.SET_NULL,
        related_name='news',
        null=True,
        verbose_name="Источник",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Новости"
        verbose_name_plural = verbose_name
        ordering = ["-published_at"]
        indexes = [
            models.Index(fields=["-published_at"])
        ]


class Source(models.Model):
    link = models.URLField()
    active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    categories = models.ManyToManyField("Category", through="SourceCategory", related_name="sources", blank=True)

    def __str__(self):
        return self.link


class Category(models.Model):  # Категории
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, db_index=True)

    def __str__(self):
        return self.name


class SourceCategory(models.Model):  # Ассоциативная таблица источника-категория
    source = models.ForeignKey(Source, on_delete=models.CASCADE, related_name="source_categories")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="source_categories")


class NewsImage(models.Model):  # Прикрепленные к новости изображения
    url = models.URLField()

    news = models.OneToOneField(News, on_delete=models.CASCADE, related_name='news_image')
