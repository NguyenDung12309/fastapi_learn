from typing import Sequence
from uuid import UUID

from fastapi import APIRouter, status, HTTPException
import json

from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.book.models import BookModel
from src.book.schemas import Book, BookCreateReq, BookBase, BookUpdateReq
from src.book.services import BookService
from src.db.main import get_session

book_router = APIRouter()
book_service = BookService()

@book_router.get("/", response_model=list[BookModel])
async def get_all_books(session: AsyncSession = Depends(get_session)) -> Sequence[BookModel]:
    books =await book_service.get_all_book(session)
    return books

@book_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_a_book(payload: BookCreateReq, session: AsyncSession = Depends(get_session)) -> BookModel:
    response = await book_service.create_book(payload, session)

    return response

@book_router.get("/{book_uid}")
async def get_book_by_id(book_uid: UUID, session: AsyncSession = Depends(get_session)) -> BookModel:
    response = await book_service.get_book_by_id(book_uid, session)

    return response

@book_router.patch("/{book_uid}", response_model=BookModel)
async def update_a_book(book_uid: UUID,payload: BookUpdateReq, session: AsyncSession = Depends(get_session)) -> BookModel:
    response = await book_service.update_book(book_uid, payload, session)

    return response

@book_router.delete("/{book_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_a_book(book_uid: UUID, session: AsyncSession = Depends(get_session)):
    response = await book_service.delete_book(book_uid, session)

    if not response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return response


