from abc import ABC

from pydantic import BaseModel, field_serializer
from datetime import datetime


class NewsPublishedAtMixin(ABC):
    @field_serializer("published_at")
    def serialize_dt(self, dt: datetime) -> str:
        return dt.strftime("%H:%M | %d.%m.%Y ")


class NewsCategory(BaseModel):
    id: int
    name: str
    slug: str


class NewsCategoriesOutputModel(NewsCategory):
    children: list["NewsCategoriesOutputModel"]


class NewsOutputModel(BaseModel, NewsPublishedAtMixin):
    id: int
    title: str
    published_at: datetime
    categories: list[NewsCategory]


class NewsByIdOutputModel(BaseModel, NewsPublishedAtMixin):
    title: str
    body: str
    published_at: datetime
    categories: list[NewsCategory]
