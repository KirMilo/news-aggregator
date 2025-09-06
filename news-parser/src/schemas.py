from pydantic import BaseModel, HttpUrl, field_serializer
from datetime import datetime
from typing import List


class UpdatedSource(BaseModel):
    id: int
    updated_at: datetime

    @field_serializer("updated_at")
    def serialize_dt(self, dt: datetime) -> str:
        return dt.isoformat()

class Source(UpdatedSource):
    link: HttpUrl

    @field_serializer("link")
    def serialize_link(self, link: HttpUrl) -> str:
        return str(link)


class News(BaseModel):
    title: str
    body: str | None = None
    link: HttpUrl
    published_at: datetime

    @field_serializer("published_at")
    def serialize_dt(self, dt: datetime) -> str:
        return dt.isoformat()

    @field_serializer("link")
    def serialize_link(self, link: HttpUrl) -> str:
        return str(link)

class ParsedNews(BaseModel):
    source: UpdatedSource
    news: List[News]


class CreateNews(BaseModel):
    data: List[ParsedNews]
