from django.db import models


class Source(models.Model):
    link = models.URLField()
    active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    categories = models.ManyToManyField("Category", through="SourceCategory", related_name="sources", blank=True)

    def __str__(self):
        return self.link
