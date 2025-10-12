from django.db import models


class SourceCategory(models.Model):  # Ассоциативная таблица источника-категория
    source = models.ForeignKey("Source", on_delete=models.CASCADE, related_name="source_categories")
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="source_categories")
