from uuid import UUID

from src.core.exceptions import ConflictError
from src.models.categories_model import CategoryModel
from src.repositories.categories_repository import CategoryRepository
from src.schemas.category_schema import CategoryCreateSchema, CategoryUpdateSchema
from src.services.base_service import BaseService


class CategoryService(BaseService):
    def __init__(self, repository: CategoryRepository):
        super().__init__(repository, CategoryModel)

    def create(self, schema: CategoryCreateSchema):
        existing = self._repository.get_by_name(schema.name)

        if existing:
            raise ConflictError(conflicts={"name": schema.name})

        data = CategoryModel(**schema.model_dump())
        return self._repository.create(data)

    def update(self, uid: str, schema: CategoryUpdateSchema):
        instance = self._repository.get_by_id(UUID(uid))
        update_data = schema.model_dump(exclude_unset=True)
        new_name = update_data.get("name")

        if new_name and new_name != instance.name:
            existing_category = self._repository.get_by_name(new_name)
            if existing_category:
                raise ConflictError(conflicts={"name": new_name})

        for key, value in update_data.items():
            setattr(instance, key, value)

        return self._repository.update(instance)
