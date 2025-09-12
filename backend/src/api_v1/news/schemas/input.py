from typing import Annotated
from fastapi import Query
from pydantic import BaseModel


class NewsParams(BaseModel):
    page: Annotated[int | None, Query(title="Page number", ge=1, default=1)]
    limit: Annotated[int | None, Query(title="Max items", ge=1, le=100, default=10)]
    category: Annotated[str | None, Query(title="Category Slug", max_length=70)] = None
