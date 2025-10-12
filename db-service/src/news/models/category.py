from django.db import models


class Category(models.Model):  # Категории
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, db_index=True)
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, default=None)

    def __str__(self):
        return self.name
