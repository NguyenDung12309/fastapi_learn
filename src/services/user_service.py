from uuid import UUID

from src.common.matrix_permission import ROLE_PERMISSIONS
from src.core.exceptions import NotFoundError, UnauthorizedError
from src.core.security import password_hasher
from src.repositories.user_repository import UserRepository
from src.schemas.auth_schema import ChangePasswordRequestSchema
from src.schemas.user_schema import GetMeResponseSchema
from src.services.base_service import ReadMixin


class UserService(ReadMixin[UserRepository]):
    def __init__(self, repository: UserRepository):
        super().__init__(repository)

    def get_me(self, user_id: UUID) -> GetMeResponseSchema:
        user = self.get_by_id(user_id)

        if not user:
            raise NotFoundError(resource_details={"id": str(user_id)})

        user_data = user.model_dump()

        user_data["permissions"] = ROLE_PERMISSIONS.get(user.role, [])

        return GetMeResponseSchema(**user_data)

    def update_password(self, user_id: UUID, schema: ChangePasswordRequestSchema):
        error_msg = "Tài khoản hoặc mật khẩu không chính xác"
        user_info = self.get_by_id(user_id)
        is_valid_pass = password_hasher.verify(schema.old_password, user_info.password)
        if not is_valid_pass:
            raise UnauthorizedError(error_msg)
        user_info.password = password_hasher.hash(schema.new_password)
        return self.update(instance=user_info, schema=user_info)
