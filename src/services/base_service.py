from typing import TypeVar, Generic, Sequence, Type
from uuid import UUID

from pydantic import BaseModel

from src.models.base_table_model import BaseTableModel
from src.repositories.base_repository import BaseRepository

T = TypeVar('T', bound=BaseTableModel)
TCreate = TypeVar('TCreate', bound=BaseModel)
TUpdate = TypeVar('TUpdate', bound=BaseModel)


class BaseService(Generic[T, TCreate, TUpdate]):
    def __init__(self, repository: BaseRepository[T], model_class: Type[T]):
        self._repository = repository
        self._model_class = model_class

    def get_all(self) -> Sequence[T]:
        return self._repository.get_all()

    def get_by_id(self, uid: UUID) -> T:
        return self._repository.get_by_id(uid)

    def create(self, schema: TCreate):
        data = self._model_class(**schema.model_dump())
        return self._repository.create(data)

    def update(self, uid: UUID, schema: TUpdate):
        info = self._repository.get_by_id(uid)
        update_data = schema.model_dump()
        for key, value in update_data.items():
            setattr(info, key, value)

        return self._repository.update(info)
