from typing import Annotated

from aiohttp import ClientSession
from fastapi import APIRouter, Depends, Path, Query, HTTPException
from starlette.websockets import WebSocket, WebSocketState

from api_v1.news.schemas.input import NewsParams, FreshNewsParams
from api_v1.news.schemas.output import NewsOutputModel, NewsByIdOutputModel, NewsCategoriesOutputModel
from api_v1.utils.validate_response import validate_response
from core.http_session import get_http_session
from rabbit.news import NewsMessagesQueue, get_news_messages_queue

NEWS_ENDPOINT = "/api/v1/news/"
FRESH_NEWS_ENDPOINT = "/api/v1/news/fresh/"
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
    validate_response(response.status)
    data = await response.json()
    return data["results"]


@router.get("")
async def get_news(
        params: NewsParams = Depends(NewsParams),
        session: ClientSession = Depends(get_http_session),
) -> NewsOutputModel:
    response = await session.get(
        NEWS_ENDPOINT,
        params=params.model_dump(exclude_none=True)
    )
    validate_response(response.status)
    data = await response.json()
    if data:
        return NewsOutputModel(
            next=data[-1]["published_at"],
            previous=data[0]["published_at"],
            data=data,
        )
    raise HTTPException(
        status_code=404,
        detail="Not found",
    )


@router.get("/fresh")
async def get_fresh_news(
        params: NewsParams = Depends(FreshNewsParams),
        session: ClientSession = Depends(get_http_session),
) -> NewsOutputModel:
    response = await session.get(
        FRESH_NEWS_ENDPOINT,
        params=params.model_dump(exclude_none=True)
    )
    validate_response(response.status)
    data = await response.json()
    if data:
        return NewsOutputModel(
            next=data[0]["published_at"],
            previous=data[-1]["published_at"],
            data=data,
        )
    raise HTTPException(
        status_code=404,
        detail="Not found",
    )


@router.get("/{news_id}")
async def get_news_by_id(
        news_id: Annotated[int, Path(title="News ID", ge=1)],
        session: ClientSession = Depends(get_http_session),
) -> NewsByIdOutputModel:
    response = await session.get(NEWS_ENDPOINT + "%d/" % news_id, )
    validate_response(response.status)
    return await response.json()


@router.websocket("/updates")
async def news_updates(
        websocket: WebSocket,
        queue: NewsMessagesQueue = Depends(get_news_messages_queue),
):
    await websocket.accept()
    queue.set_websocket(websocket)
    await queue.send_update_on_receipt()

    while websocket.client_state == WebSocketState.CONNECTED:
        await websocket.receive()
