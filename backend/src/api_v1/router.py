from fastapi import APIRouter
from api_v1 import news, comments, users, auth



router = APIRouter()
router.include_router(comments.router)
router.include_router(news.router)
router.include_router(users.router)
router.include_router(auth.router)
