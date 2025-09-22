from datetime import datetime

from django.contrib import admin
from news.models import News, Source


# admin.site.register(News)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "published_at", "link", "active", "source")

    def get_changeform_initial_data(self, request):
        return {
            "source": Source.objects.get(link="https://news-aggregator/"),
            "published_at": datetime.now()
        }
