from datetime import date
from typing import List

from sqlmodel import Relationship

from src.models.base_table_model import BaseTableModel
from src.models.book_categories_link import BookCategoryLink


class BookModel(BaseTableModel, table=True):
    __tablename__ = "book"
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    category: List["CategoryModel"] = Relationship(back_populates="books", link_model=BookCategoryLink)
