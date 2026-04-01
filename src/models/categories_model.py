from typing import List, TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship

from src.models.base_table_model import BaseTableModel
from src.models.book_categories_link import BookCategoryLink

if TYPE_CHECKING:
    from src.models.book_model import BookModel


class CategoryModel(BaseTableModel, table=True):
    __tablename__ = 'category'
    name: str = Field(unique=True, index=True)
    description: Optional[str] = Field(default=None, max_length=100)
    books: List["BookModel"] = Relationship(
        back_populates='category', link_model=BookCategoryLink
    )
