from typing import Annotated

from aiohttp import ClientSession
from fastapi import APIRouter, Depends, Path, Query

from api_v1.news.schemas.input import NewsParams
from api_v1.news.schemas.output import NewsOutputModel, NewsByIdOutputModel
from core.http_session import get_http_session

router = APIRouter(
    tags=["News"],
    prefix="/news"
)


FRESH_NEWS_ENDPOINT = "/api/v1/news"
NEWS_BY_ID_ENDPOINT = "/api/v1/news/%d"
SEARCH_NEWS_ENDPOINT = "/api/v1/news/search"


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
    data = await response.json()
    return data["results"]


@router.get("/{news_id}")
async def get_news_by_id(
        news_id: Annotated[int, Path(title="News ID", ge=1)],
        session: ClientSession = Depends(get_http_session),
) -> NewsByIdOutputModel:
    response = await session.get(NEWS_BY_ID_ENDPOINT % news_id,)
    data = await response.json()
    return data
