from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import List


class Source(BaseModel):
    id: int
    link: HttpUrl
    updated_at: datetime


class Resource(BaseModel):
    source: Source
    categories: List[int]

class News(BaseModel):
    title: str
    body: str | None = None
    link: HttpUrl


class ProcessingNews(News):
    published_at: datetime


class ParsedNews(Resource):
    data: List[News]
