from abc import ABC
from datetime import datetime

from pydantic import BaseModel, field_serializer


class NewsPublishedAtMixin(ABC):
    @field_serializer("date_joined")
    def serialize_dt(self, dt: datetime) -> str:
        return dt.strftime("%d.%m.%Y")


class UserProfileModel(BaseModel):
    username: str
    email: str | None = None
    avatar: str | None = None
    date_joined: datetime
