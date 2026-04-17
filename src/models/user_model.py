from typing import List

from sqlmodel import Relationship, Field

from src.models.base_table_model import BaseTableModel


class UserModel(BaseTableModel, table=True):
    __tablename__ = 'user'
    username: str = Field(unique=True)
    email: str = Field(unique=True)
    first_name: str
    last_name: str
    role: str = Field(nullable=False, default="user")
    password: str = Field(exclude=True)
    is_verified: bool
    published_books: List["BookModel"] = Relationship(back_populates="publisher")
