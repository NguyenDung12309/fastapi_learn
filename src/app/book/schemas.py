from datetime import datetime, date
from uuid import UUID

from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str

class BookCreateReq(BookBase):
    pass

class BookUpdateReq(BookBase):
    pass