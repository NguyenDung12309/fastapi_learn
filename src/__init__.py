from fastapi import FastAPI

from src.book.routes import book_router

app = FastAPI()

app.include_router(book_router, prefix="/book", tags=["book"])