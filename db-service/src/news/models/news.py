from django.db import models


class News(models.Model):  # Новости
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    body = models.TextField(verbose_name="Статья")
    published_at = models.DateTimeField(verbose_name="Дата публикации")
    link = models.URLField(verbose_name="Ссылка", null=True, blank=True)
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
