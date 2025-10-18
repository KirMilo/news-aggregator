from aiohttp import ClientSession
from fastapi import APIRouter, Depends, Response

from api_v1.auth.schemas.input import LoginUserModel, RefreshInputModel, RegisterUserModel
from api_v1.auth.schemas.output import RefreshOutputModel
from core.http_session import get_http_session
from api_v1.utils.auth import get_current_user

LOGIN_ENDPOINT = "/api/v1/auth/login/"
LOGOUT_ENDPOINT = "/api/v1/auth/logout/"
REGISTER_ENDPOINT = "/api/v1/auth/register/"
REFRESH_TOKEN_ENDPOINT = "/api/v1/auth/token/refresh/"

router = APIRouter(
    tags=["auth"],
    prefix="/auth"
)


@router.post("/login")
async def login(
        form: LoginUserModel,
        session: ClientSession = Depends(get_http_session),
) -> RefreshOutputModel:
    response = await session.post(
        LOGIN_ENDPOINT,
        json=form.model_dump(exclude_unset=True, exclude_none=True),
    )
    return await response.json()


@router.post("/logout")
async def logout(
        form: RefreshInputModel,
        session: ClientSession = Depends(get_http_session),
):
    response = await session.post(
        LOGOUT_ENDPOINT,
        json=form.model_dump()
    )
    return Response(status_code=response.status, content=await response.json())

@router.post("/register")
async def register(
        form: RegisterUserModel,
        session: ClientSession = Depends(get_http_session),
) -> RefreshOutputModel:
    response = await session.post(
        REGISTER_ENDPOINT,
        json=form.model_dump()
    )
    response.raise_for_status()
    return await response.json()


@router.post("/token/refresh")
async def refresh_token(
        form: RefreshInputModel,
        session: ClientSession = Depends(get_http_session),
) -> RefreshOutputModel:
    response = await session.post(
        REFRESH_TOKEN_ENDPOINT,
        json=form.model_dump()
    )
    response.raise_for_status()
    return await response.json()


@router.get("/user/authenticated")
async def is_authenticated(
        user_id: int = Depends(get_current_user),  # noqa
):
    return {"user_id": user_id}
