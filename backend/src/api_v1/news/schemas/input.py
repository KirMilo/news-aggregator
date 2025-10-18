from datetime import datetime
from typing import Annotated
from fastapi import Query
from pydantic import BaseModel, field_serializer


class NewsParams(BaseModel):
    offset: Annotated[int | None, Query(title="DateTime offset (gt)")] = None
    limit: Annotated[int | None, Query(title="Max items", ge=1, le=100, default=10)]
    category: Annotated[str | None, Query(title="Category Slug", max_length=70)] = None

    @field_serializer("offset")
    def serialize_dt(self, dt: int | None) -> str | None:
        if dt:
            return datetime.fromtimestamp(dt).isoformat()
        return None

class FreshNewsParams(NewsParams):
    offset: Annotated[int | datetime | None, Query(title="DateTime offset (lt)")] = None
