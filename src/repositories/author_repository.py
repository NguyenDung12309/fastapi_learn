from sqlmodel import select

from src.models import AuthorModel
from src.repositories.base_repository import BaseRepository


class AuthorRepository(BaseRepository[AuthorModel]):
    model_class = AuthorModel

    def get_by_name(self, name: str) -> AuthorModel | None:
        statement = select(AuthorModel).where(AuthorModel.name == name.lower())
        return self._session.exec(statement).first()
