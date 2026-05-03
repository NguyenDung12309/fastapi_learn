from uuid import UUID

from sqlalchemy import delete
from sqlmodel import Session, select

from src.core.exceptions import NotFoundError


class BaseRepository:
    def __init__(self, model, session: Session):
        self._model = model
        self._session = session

    def get_by_id(self, uid: UUID):
        data = self._session.get(self._model, uid)
        if not data:
            raise NotFoundError(resource_details={"id": str(uid)})
        return data

    def create(self, data):
        self._session.add(data)
        self._session.commit()
        self._session.refresh(data)
        return data

    def update(self, data):
        self._session.add(data)
        self._session.commit()
        self._session.refresh(data)
        return data

    def get_all(self):
        statement = select(self._model)
        return self._session.exec(statement).all()

    def delete(self, uid: UUID) -> None:
        statement = delete(self._model).where(getattr(self._model, "id") == uid)
        self._session.exec(statement)
        self._session.commit()
