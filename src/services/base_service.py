from typing import TypeVar, Generic
from uuid import UUID

from src.repositories.base_repository import BaseRepository

RepositoryT = TypeVar("RepositoryT", bound=BaseRepository)
RepoT = TypeVar("RepoT", bound=BaseRepository)


class CRUDMixin(Generic[RepoT]):
    def __init__(self, repository: RepoT):
        self._repository = repository

    def get_all(self):
        return self._repository.get_all()

    def get_by_id(self, uid: UUID):
        return self._repository.get_by_id(uid)
