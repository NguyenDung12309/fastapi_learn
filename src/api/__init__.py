from fastapi import APIRouter

from src.api.auth import auth_router
from src.api.author import author_router
from src.api.categories import category_router
from src.api.media import media_router
from src.api.user import user_router

api_router = APIRouter()

api_router.include_router(category_router, prefix="/category", tags=["category"])
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(user_router, prefix="/user", tags=["user"])
api_router.include_router(author_router, prefix="/author", tags=["author"])
api_router.include_router(media_router, prefix="/media", tags=["media"])
