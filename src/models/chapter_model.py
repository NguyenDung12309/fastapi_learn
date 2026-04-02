from uuid import UUID

from sqlmodel import Field, Relationship

from src.models.base_table_model import BaseTableModel


class ChapterModel(BaseTableModel, table=True):
    __tablename__ = "chapter"
    title: str
    content: str
    order: int
    book_id: UUID = Field(foreign_key="book.id")
    book: "BookModel" = Relationship(back_populates="chapters")
