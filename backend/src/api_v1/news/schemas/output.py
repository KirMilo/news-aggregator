from pydantic import BaseModel
from datetime import datetime


class NewsOutputModel(BaseModel):
    title: str
    body: str
    published_at: datetime
    categories: list[str]


class NewsByIdOutputModel(BaseModel):
    title: str
    body: str
    published_at: datetime
    categories: list[str]  # TODO: list CatogoryModel или на фронте поправить


