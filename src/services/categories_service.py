from uuid import UUID

from src.core.exceptions import ConflictError
from src.models.categories_model import CategoryModel
from src.repositories.categories_repository import CategoryRepository
from src.schemas.category_schema import CategoryCreateSchema, CategoryUpdateSchema
from src.services.base_service import CRUDMixin


class CategoryService(CRUDMixin[CategoryRepository]):
    def __init__(self, repository: CategoryRepository):
        super().__init__(repository)

    def create(self, schema: CategoryCreateSchema) -> CategoryModel:
        if self._repository.get_by_name(schema.name):
            raise ConflictError(conflicts={"name": schema.name})
        return self._repository.save(CategoryModel(**schema.model_dump()))

    def update(self, uid: str, schema: CategoryUpdateSchema) -> CategoryModel:
        instance = self._repository.get_by_id(UUID(uid))
        new_name = schema.name
        if new_name and new_name != instance.name:
            if self._repository.get_by_name(new_name):
                raise ConflictError(conflicts={"name": new_name})
        for key, value in schema.model_dump(exclude_unset=True).items():
            setattr(instance, key, value)
        return self._repository.save(instance)
