from typing import Optional, List
from uuid import UUID

from sqlmodel import Field, Relationship

from src.models.base_table_model import BaseTableModel


class AuthorModel(BaseTableModel, table=True):
    __tablename__ = "author"

    name: str = Field(index=True)
    user_id: Optional[UUID] = Field(default=None, foreign_key="user.id", nullable=True)
    books: List["BookModel"] = Relationship(back_populates="author")
