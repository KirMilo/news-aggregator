from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import News


@registry.register_document
class NewsDocument(Document):
    categories = fields.ListField(
        fields.ObjectField(
            properties={
                "id": fields.IntegerField(),
                "name": fields.TextField(),
                "slug": fields.TextField(),
            }
        )
    )

    def prepare_categories(self, instance):  # noqa
        return [
            {
                "id": cat.id,
                "name": cat.name,
                "slug": cat.slug,
            }
            for cat in instance.source.categories.all()
        ]

    class Index:
        name = "news"
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0,
        }

    class Django:
        model = News

        fields = [
            "id",
            "title",
            "body",
            "published_at",
            "active",
        ]
