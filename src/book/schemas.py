from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str

class Book(BookBase):
    id: int

class BookCreateModel(BookBase):
    pass