from fastapi import APIRouter

from src.app.book.routes import book_router

api_router = APIRouter()

api_router.include_router(book_router, prefix="/books", tags=["Books"])