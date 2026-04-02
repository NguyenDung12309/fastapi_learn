from datetime import date
from enum import StrEnum
from typing import List, Optional
from uuid import UUID

from sqlmodel import Relationship, Field

from src.models.base_table_model import BaseTableModel
from src.models.book_categories_link import BookCategoryLink


class BookModel(BaseTableModel, table=True):
    __tablename__ = "book"

    class BookStatus(StrEnum):
        ONGOING = "ongoing"
        COMPLETED = "completed"
        DROPPED = "dropped"

    title: str = Field(index=True)
    slug: str = Field(unique=True, index=True)
    author_id: UUID = Field(foreign_key="user.id")
    author: "AuthorModel" = Relationship(back_populates="books")
    description: str
    publisher_id: UUID = Field(foreign_key="user.id")
    publisher: "UserModel" = Relationship(back_populates="published_books")
    published_date: date
    image: Optional[str] = Field(default=None, nullable=True)
    status: BookStatus = Field(default=BookStatus.ONGOING)
    view_count: int = Field(default=0)
    rating: int
    category: List["CategoryModel"] = Relationship(back_populates="books", link_model=BookCategoryLink)
    chapters: List["ChapterModel"] = Relationship(back_populates="book")
