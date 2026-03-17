from fastapi import APIRouter, status, HTTPException
import json
from src.book.data import books
from src.book.schemas import Book, BookCreateModel

book_router = APIRouter()

def pretty_print(data):
    if isinstance(data, list):
        data = [d.model_dump() if hasattr(d, "model_dump") else d for d in data]
    elif hasattr(data, "model_dump"):
        data = data.model_dump()

    print(json.dumps(data, indent=2, ensure_ascii=False))

def generate_id():
    if not books:
        return 1
    return max(book.id for book in books) + 1

@book_router.get("/", response_model=list[Book])
async def get_all_books() -> list[Book]:
    return books

@book_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_a_book(payload: BookCreateModel) -> Book:
    new_book = payload.model_dump()
    new_book["id"] = generate_id()
    books.append(Book(**new_book))
    pretty_print(books)
    return new_book

@book_router.get("/{book_id}")
async def get_a_book(book_id: int) -> Book:
    for book in books:
        if book.id == book_id:
            return book
    raise HTTPException(
        status_code=404,
        detail=f"Book with id {book_id} not found"
    )

@book_router.patch("/{book_id}")
async def update_a_book(book_id: int,payload: Book):
    for index, book in enumerate(books):
        if book.id == book_id:
            books[index] = Book(**payload.model_dump())
            return books[index]
    raise HTTPException(
        status_code=404,
        detail=f"Book with id {book_id} not found"
    )

@book_router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_a_book(book_id: int):
    for book in books:
        if book.id == book_id:
            books.remove(book)
            return
    raise HTTPException(
        status_code=404,
        detail=f"Book with id {book_id} not found"
    )
