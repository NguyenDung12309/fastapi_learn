from typing import Optional

from sqlmodel import select

from src.models import UserModel
from src.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[UserModel]):
    def __init__(self, session):
        super().__init__(UserModel, session)

    def get_user_by_email(self, email: str) -> Optional[UserModel]:
        statement = select(UserModel).where(UserModel.email == email)
        result = self._session.exec(statement).first()
        return result

    def get_user_by_username(self, username: str) -> Optional[UserModel]:
        statement = select(UserModel).where(UserModel.username == username)
        result = self._session.exec(statement).first()
        return result
