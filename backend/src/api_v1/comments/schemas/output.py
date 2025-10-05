from pydantic import BaseModel


class NewsCommentOutputModel(BaseModel):
    id: int
    username: str
    avatar: str | None = None
