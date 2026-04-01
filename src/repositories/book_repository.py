from src.models.book_model import BookModel
from src.repositories.base_repository import BaseRepository


class BookRepository(BaseRepository[BookModel]):
    def __init__(self, session):
        super().__init__(BookModel, session)
