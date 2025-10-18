from aiohttp import ClientSession
from fastapi import APIRouter, Depends, HTTPException, UploadFile, Request, Response

from api_v1.users.schemas.output import UserProfileModel, UserProfilePartialOutputModel
from api_v1.users.validate_image import validate_image
from core.http_session import get_http_session
from api_v1.utils.auth import get_current_user
from s3.client import s3_client

router = APIRouter(
    tags=["users"],
    prefix="/user",
)

USER_PROFILE_ENDPOINT = "/api/v1/user/%d/"
UPLOAD_AVATAR_ENDPOINT = "/api/v1/user/"

EXCLUDE_HEADERS = {"content-type", "content-length"}


@router.put("/avatar")
async def upload_avatar(
        request: Request,
        image: UploadFile = Depends(validate_image),
        user_id: int = Depends(get_current_user),
        session: ClientSession = Depends(get_http_session),
) -> UserProfilePartialOutputModel:
    file = image.file
    filename = f"{user_id}_{image.filename}"
    await s3_client.upload_file(file, filename)
    response = await session.patch(
        UPLOAD_AVATAR_ENDPOINT,
        headers={key: value for key, value in request.headers.items() if key not in EXCLUDE_HEADERS},
        json={"avatar": filename},
    )
    response.raise_for_status()
    return await response.json()


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
