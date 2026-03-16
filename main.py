from fastapi import FastAPI
from typing import Optional

from pydantic import BaseModel
from starlette import status

books = [
    {
        "id": 1,
        "title": "Think Python",
        "author": "Allen B. Downey",
        "publisher": "O'Reilly Media",
        "published_date": "2021-01-01",
        "page_count": 1234,
        "language": "English",
    },
    {
        "id": 2,
        "title": "Django By Example",
        "author": "Antonio Mele",
        "publisher": "Packt Publishing Ltd",
        "published_date": "2022-01-19",
        "page_count": 1023,
        "language": "English",
    },
]

app = FastAPI()

class Book(BaseModel):
    id: int
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str

@app.get("/books", response_model=list[Book])
async def get_all_books() -> list[Book]:
    return books

@app.post("/book", status_code=status.HTTP_201_CREATED)
async def create_a_book(payload: Book) -> Book:
    new_book = payload.model_dump()
    books.append(new_book)
    return new_book

@app.get("/book/{id}")
async def get_a_book(id: int):
    pass

@app.post("/book/{id}")
async def update_a_book(id: int):
    pass

@app.get("/book/{id}")
async def delete_a_book(id: int):
    pass
