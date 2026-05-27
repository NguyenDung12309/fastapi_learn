from src.models.book_model import BookModel
from src.repositories.base_repository import BaseRepository


class BookRepository(BaseRepository[BookModel]):
    model_class = BookModel
