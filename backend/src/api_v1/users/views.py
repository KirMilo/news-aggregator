from typing import Annotated

from aiohttp import ClientSession
from fastapi import APIRouter, Depends, HTTPException, UploadFile, Request, security, Header
from fastapi.security import HTTPAuthorizationCredentials

from api_v1.users.schemas.output import UserProfileModel
from core.http_session import get_http_session
from api_v1.utils import http_bearer

router = APIRouter(
    tags=["users"],
    prefix="/user",
)


USER_PROFILE_ENDPOINT = "/api/v1/user/%d/"
UPLOAD_AVATAR_ENDPOINT = "/api/v1/user/avatar/"


@router.get("/user/authenticated")
async def is_authenticated(
        request: Request,
        auth = Depends(http_bearer),  # noqa
        session: ClientSession = Depends(get_http_session),
):
    response = await session.get("/api/v1/user/authenticated", headers=request.headers)
    return await response.json()


@router.post("/avatar")
async def upload_avatar(
    uploaded_file: UploadFile,
    request: Request,
    auth = Depends(http_bearer),
):
    file = uploaded_file.file
    filename = uploaded_file.filename


@router.get("/{user_id}")
async def get_user(
        user_id: int,
        request: Request,
        session: ClientSession = Depends(get_http_session),

) -> UserProfileModel:
    response = await session.get(USER_PROFILE_ENDPOINT % user_id, headers=request.headers)
    if response.status != 200:
        raise HTTPException(
            response.status,
            await response.json()
        )
    return await response.json()
