from typing import Annotated

from aiohttp import ClientSession
from fastapi import APIRouter, Depends, Path, Query, HTTPException
from starlette.websockets import WebSocket

from api_v1.news.schemas.input import NewsParams, FreshNewsParams
from api_v1.news.schemas.output import NewsOutputModel, NewsByIdOutputModel, NewsCategoriesOutputModel
from api_v1.utils.ws_manager import WebSocketManager
from core.http_session import get_http_session
from rabbit.news import NewsMessagesQueue, get_news_messages_queue

FRESH_NEWS_ENDPOINT = "/api/v1/news/"
NEWS_BY_ID_ENDPOINT = "/api/v1/news/%d/"
SEARCH_NEWS_ENDPOINT = "/api/v1/news/search"
NEWS_CATEGORIES_ENDPOINT = "/api/v1/news/categories/"

router = APIRouter(
    tags=["News"],
    prefix="/news"
)


@router.get("/categories")
async def get_news_categories(
        session: ClientSession = Depends(get_http_session),
) -> list[NewsCategoriesOutputModel]:
    response = await session.get(NEWS_CATEGORIES_ENDPOINT)
    return await response.json()


@router.get("/search")
async def search_news(
        search: Annotated[str, Query(title="Search query", min_length=3, max_length=120)],
        session: ClientSession = Depends(get_http_session),
) -> list[NewsOutputModel]:
    response = await session.get(SEARCH_NEWS_ENDPOINT, params={"search": search})
    data = await response.json()
    return data["results"]


@router.get("")
async def get_news(
        params: NewsParams = Depends(NewsParams),
        session: ClientSession = Depends(get_http_session),
) -> list[NewsOutputModel]:
    response = await session.get(
        "/api/v1/news",
        params=params.model_dump(exclude_none=True)
    )
    return await response.json()


@router.get("/fresh")
async def get_fresh_news(
        params: NewsParams = Depends(FreshNewsParams),
        session: ClientSession = Depends(get_http_session),
) -> list[NewsOutputModel]:
    response = await session.get(
        "/api/v1/news/fresh",
        params=params.model_dump(exclude_none=True)
    )
    return await response.json()


@router.get("/{news_id}")
async def get_news_by_id(
        news_id: Annotated[int, Path(title="News ID", ge=1)],
        session: ClientSession = Depends(get_http_session),
) -> NewsByIdOutputModel:
    response = await session.get(NEWS_BY_ID_ENDPOINT % news_id, )
    if response.status == 404:
        raise HTTPException(status_code=404, detail="Not found")
    return await response.json()


@router.websocket("/updates")
async def news_updates(
        websocket: WebSocket,
        queue: NewsMessagesQueue = Depends(get_news_messages_queue),
):
    async with WebSocketManager(websocket):
        queue.set_websocket(websocket)
        while True:
            await queue.send_update_on_receipt()
