from datetime import datetime
from typing import Annotated
from fastapi import Query
from pydantic import BaseModel


class NewsParams(BaseModel):
    offset: Annotated[datetime | None, Query(title="DateTime offset (gt)")] = None
    limit: Annotated[int | None, Query(title="Max items", ge=1, le=100, default=10)]
    category: Annotated[str | None, Query(title="Category Slug", max_length=70)] = None


class FreshNewsParams(NewsParams):
    offset: Annotated[datetime, Query(title="DateTime offset (lt)")] = None
