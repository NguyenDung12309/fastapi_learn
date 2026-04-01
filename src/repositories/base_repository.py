from typing import Generic, TypeVar, Type, Sequence
from uuid import UUID

from sqlmodel import Session, select

from src.core.exceptions import NotFoundError
from src.models.base_table_model import BaseTableModel

T = TypeVar("T", bound=BaseTableModel)


class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], session: Session):
        self._model = model
        self._session = session

    def get_by_id(self, uid: UUID) -> T:
        data = self._session.get(self._model, uid)
        if data is None:
            raise NotFoundError()
        return data

    def create(self, data: T) -> T:
        self._session.add(data)
        self._session.commit()
        self._session.refresh(data)
        return data

    def get_all(self) -> Sequence[T]:
        statement = select(self._model)
        return self._session.exec(statement).all()

    def update(self, data: T) -> T:
        self._session.add(data)
        self._session.commit()
        self._session.refresh(data)
        return data
