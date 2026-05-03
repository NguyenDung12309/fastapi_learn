from typing import TypeVar, Generic
from uuid import UUID

from src.repositories.base_repository import BaseRepository

RepositoryT = TypeVar("RepositoryT", bound=BaseRepository)


class BaseService(Generic[RepositoryT]):
    def __init__(self, repository: BaseRepository, model_class):
        self._repository: RepositoryT = repository
        self._model_class = model_class

    def get_all(self):
        return self._repository.get_all()

    def get_by_id(self, uid: UUID):
        return self._repository.get_by_id(uid)

    def create(self, schema):
        data = self._model_class(**schema.model_dump())
        return self._repository.create(data)

    def update(self, instance, schema):
        update_data = schema.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(instance, key, value)

        return self._repository.update(instance)

    def delete_by_id(self, uid: UUID):
        self._repository.delete(uid)
