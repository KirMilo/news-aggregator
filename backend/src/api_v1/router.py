from fastapi import APIRouter
from api_v1 import news, categories, comments, users



router = APIRouter()
router.include_router(news.router)