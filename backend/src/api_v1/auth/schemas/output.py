from pydantic import BaseModel


class RefreshOutputModel(BaseModel):
    access: str
    refresh: str
