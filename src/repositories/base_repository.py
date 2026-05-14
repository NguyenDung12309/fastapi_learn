# src/repositories/base_repository.py
from typing import Generic, TypeVar, Type, Sequence
from uuid import UUID

from sqlalchemy import delete
from sqlmodel import Session, SQLModel, select

from src.core.exceptions import NotFoundError

ModelT = TypeVar("ModelT", bound=SQLModel)


class BaseRepository(Generic[ModelT]):
    model_class: Type[ModelT]

    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, uid: UUID) -> ModelT:
        data = self._session.get(self.model_class, uid)
        if not data:
            raise NotFoundError(resource_details={"id": str(uid)})
        return data

    def get_all(self) -> Sequence[ModelT]:
        return self._session.exec(select(self.model_class)).all()

    def save(self, data: ModelT) -> ModelT:
        self._session.add(data)
        self._session.commit()
        self._session.refresh(data)
        return data

    def delete(self, uid: UUID) -> None:
        self._session.exec(delete(self.model_class).where(
            getattr(self.model_class, "id") == uid
        ))
        self._session.commit()
