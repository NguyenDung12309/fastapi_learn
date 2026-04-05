from src.core.security import PasswordHasher
from src.models import UserModel
from src.repositories.user_repository import UserRepository
from src.schemas.user_schema import UserCreateSchema
from src.services.base_service import BaseService


class UserService(BaseService[UserModel, UserCreateSchema, UserModel]):
    def __init__(self, repository: UserRepository):
        self.user_repository = repository
        super().__init__(repository, UserModel)

    def create(self, schema: UserCreateSchema):
        user_data = schema.model_dump()
        if "password" in user_data:
            user_data["password"] = PasswordHasher.hash(user_data["password"])
        data = self._model_class(**user_data)
        return self._repository.create(data)
