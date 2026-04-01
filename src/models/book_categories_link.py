from uuid import UUID

from sqlmodel import SQLModel, Field


class BookCategoryLink(SQLModel, table=True):
    __tablename__ = 'book_category_link'
    book_id: UUID = Field(foreign_key='book.id', primary_key=True)
    category_id: UUID = Field(foreign_key='category.id', primary_key=True)
