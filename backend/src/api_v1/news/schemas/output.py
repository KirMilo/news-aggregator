from abc import ABC

from pydantic import BaseModel, field_serializer
from datetime import datetime


class NewsPublishedAtMixin(ABC):
    @field_serializer("published_at")
    def serialize_dt(self, dt: datetime) -> str:
        return dt.strftime("%H:%M | %d.%m.%Y ")


class NewsOutputModel(BaseModel, NewsPublishedAtMixin):
    id: int  # TODO: Поправить в db_service
    title: str
    # body: str
    published_at: datetime
    categories: list[str]


class NewsByIdOutputModel(BaseModel, NewsPublishedAtMixin):
    title: str
    body: str
    published_at: datetime
    categories: list[str]  # TODO: list CatogoryModel или на фронте поправить



class NewsCategoriesOutputModel(BaseModel):
    id: int
    name: str
    slug: str
    children: list["NewsCategoriesOutputModel"]
