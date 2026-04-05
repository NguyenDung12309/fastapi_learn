from typing import Optional

from sqlmodel import select

from src.core.exceptions import ConflictError
from src.models import UserModel
from src.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[UserModel]):
    def __init__(self, session):
        super().__init__(UserModel, session)

    def _get_email(self, email: str) -> Optional[UserModel]:
        statement = select(UserModel).where(UserModel.email == email)
        result = self._session.exec(statement).first()
        return result

    def _get_username(self, username: str) -> Optional[UserModel]:
        statement = select(UserModel).where(UserModel.username == username)
        result = self._session.exec(statement).first()
        return result

    def create(self, user: UserModel):
        conflicts = {}
        if self._get_email(user.email):
            conflicts["email"] = user.email
        if self._get_username(user.username):
            conflicts["username"] = user.username
        if conflicts:
            raise ConflictError(conflicts=conflicts)
        self._session.add(user)
        self._session.commit()
        self._session.refresh(user)
        return user
