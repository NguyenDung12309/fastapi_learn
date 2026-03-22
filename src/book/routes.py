from typing import Sequence
from uuid import UUID
from fastapi import APIRouter, status
from fastapi.params import Depends
from src.book.models import BookModel
from src.book.schemas import  BookCreateReq, BookUpdateReq
from src.book.services import BookService
from src.db.main import get_session
from sqlmodel import Session

book_router = APIRouter()
book_service = BookService()

@book_router.get("/", response_model=list[BookModel])
def get_all_books(session: Session = Depends(get_session)) -> Sequence[BookModel]:
    books = book_service.get_all_book(session)
    return books

@book_router.post("/", status_code=status.HTTP_201_CREATED)
def create_a_book(payload: BookCreateReq, session: Session = Depends(get_session)) -> BookModel:
    response = book_service.create_book(payload, session)
    return response

@book_router.get("/{book_uid}")
def get_book_by_id(book_uid: UUID, session: Session = Depends(get_session)) -> BookModel:
    response = book_service.get_book_by_id(book_uid, session)
    return response

@book_router.patch("/{book_uid}", response_model=BookModel)
def update_a_book(book_uid: UUID,payload: BookUpdateReq, session: Session = Depends(get_session)) -> BookModel:
    response = book_service.update_book(book_uid, payload, session)
    return response

@book_router.delete("/{book_uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_a_book(book_uid: UUID, session: Session = Depends(get_session)):
    book_service.delete_book(book_uid, session)


