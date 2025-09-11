from django.contrib import admin
from news.models import News

# admin.site.register(News)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("title", "published_at", "link", "active")
    readonly_fields = ("published_at", "source", "link")
