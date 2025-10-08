from pydantic import BaseModel


class RefreshInputModel(BaseModel):
    refresh: str


class LoginUserModel(BaseModel):
    username: str | None = None
    email: str | None = None
    password: str


class RegisterUserModel(BaseModel):
    username: str
    email: str
    password: str
    password2: str
