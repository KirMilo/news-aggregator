from aiohttp import ClientSession
from fastapi import APIRouter, Depends, HTTPException, Response

from api_v1.auth.schemas.input import LoginUserModel, RefreshInputModel, RegisterUserModel
from api_v1.auth.schemas.output import RefreshOutputModel
from core.http_session import get_http_session

LOGIN_ENDPOINT = "/api/v1/auth/login/"
LOGOUT_ENDPOINT = "/api/v1/auth/logout/"
REGISTER_ENDPOINT = "/api/v1/auth/register/"
REFRESH_TOKEN_ENDPOINT = "/api/v1/auth/refresh/"

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
    return await response.json()


@router.post("/refresh")
async def refresh_token(
        form: RefreshInputModel,
        session: ClientSession = Depends(get_http_session),
) -> RefreshOutputModel:
    response = await session.post(
        REFRESH_TOKEN_ENDPOINT,
        json=form.model_dump()
    )
    return await response.json()
