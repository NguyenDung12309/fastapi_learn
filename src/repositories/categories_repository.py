from sqlmodel import select

from src.models.categories_model import CategoryModel
from src.repositories.base_repository import BaseRepository


class CategoryRepository(BaseRepository[CategoryModel]):
    def __init__(self, session):
        super().__init__(CategoryModel, session)

    def get_by_name(self, name: str) -> CategoryModel | None:
        statement = select(CategoryModel).where(CategoryModel.name == name)
        return self._session.exec(statement).first()
