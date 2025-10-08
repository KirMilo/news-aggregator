from typing import Annotated

from aiohttp import ClientSession
from fastapi import APIRouter, Depends, Path, Request, HTTPException
from starlette.responses import JSONResponse
from starlette.websockets import WebSocket

from api_v1.comments.schemas.output import NewsCommentOutputModel
from api_v1.comments.schemas.input import NewsCommentInputModel
from api_v1.utils import WebSocketManager, http_bearer
from core.http_session import get_http_session
from rabbit.comments import NewsCommentsMessagesQueue, get_news_comments_messages_queue

NEWS_COMMENTS_ENDPOINT = "/api/v1/news/%d/comments/"

router = APIRouter(
    tags=["NewsComments"],
    prefix="/news"
)


@router.get("/{news_id}/comments")
async def get_news_comments(
        news_id: Annotated[int, Path(title="News ID")],
        session: ClientSession = Depends(get_http_session),
) -> list[NewsCommentOutputModel]:
    response = await session.get(NEWS_COMMENTS_ENDPOINT % news_id)
    if response.status != 200:
        raise HTTPException(status_code=404, detail="Post not found")
    data = await response.json()
    return data["results"]


@router.post("/{news_id}/comment")
async def post_news_comment(
        news_id: Annotated[int, Path(title="News ID")],
        comment: NewsCommentInputModel,
        request: Request,
        session: ClientSession = Depends(get_http_session),
        credentials = Depends(http_bearer),  # noqa
):
    try:
        response = await session.post(
            NEWS_COMMENTS_ENDPOINT % news_id,
            json=comment.model_dump(),
            headers=request.headers,
        )
        if not response.status != 201:
            raise HTTPException(status_code=response.status)
    except Exception as error:  # noqa
        raise HTTPException(status_code=500, detail="Internal Server Error")

    return JSONResponse(status_code=response.status, content={"message": "Comment created successfully"})


@router.websocket("/{news_id}/comments/updates")
async def news_updates(
        websocket: WebSocket,
        queue: NewsCommentsMessagesQueue = Depends(get_news_comments_messages_queue),
):
    async with WebSocketManager(websocket):
        queue.set_websocket(websocket)
        while True:
            await queue.send_update_on_receipt()
