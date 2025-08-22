import pydantic
import datetime
from typing import List


class Source(pydantic.BaseModel):
    id: int
    link: pydantic.HttpUrl
    updated_at: datetime.datetime


class Resource(pydantic.BaseModel):
    source: Source
    categories: List[int]

class News(pydantic.BaseModel):
    title: str
    body: str | None = None
    link: pydantic.HttpUrl


class ProcessingNews(News):
    published_at: datetime.datetime


class ParsedNews(Resource):
    data: List[News]
