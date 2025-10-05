from pydantic import BaseModel


class NewsCommentInputModel(BaseModel):
    body: str
