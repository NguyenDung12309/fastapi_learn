from src.core.exceptions import ConflictError
from src.models.categories_model import CategoryModel
from src.repositories.categories_repository import CategoryRepository
from src.schemas.category_schema import CategoryCreateSchema, CategoryUpdateSchema
from src.services.base_service import BaseService


class CategoryService(BaseService[CategoryModel, CategoryCreateSchema, CategoryUpdateSchema]):
    def __init__(self, repository: CategoryRepository):
        self._category_repo = repository
        super().__init__(repository, CategoryModel)

    def create(self, schema: CategoryCreateSchema):
        existing = self._category_repo.get_by_name(schema.name)

        if existing:
            raise ConflictError(conflicts={"name": schema.name})

        return super().create(schema)
