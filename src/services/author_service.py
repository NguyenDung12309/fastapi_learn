from src.models import AuthorModel
from src.repositories.author_repository import AuthorRepository
from src.schemas.author_schema import CreateOrGetAuthorSchema
from src.services.base_service import ReadMixin


class AuthorService(ReadMixin[AuthorRepository]):
    def __init__(self, repository: AuthorRepository):
        super().__init__(repository)

    def create_or_get_author(self, schema: CreateOrGetAuthorSchema) -> AuthorModel:
        author_info = self._repository.get_by_name(schema.name)
        if author_info:
            return author_info
        new_author = AuthorModel(**schema.model_dump())
        return self._repository.save(new_author)
