from fastapi import APIRouter

from src.api.categories import category_router

api_router = APIRouter()

api_router.include_router(category_router, prefix="/category", tags=["category"])
