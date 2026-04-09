from src.core.exceptions import ConflictError, UnauthorizedError
from src.core.security import PasswordHasher
from src.core.token import TokenConfig
from src.models import UserModel
from src.models.token_model import TokenModel
from src.repositories.auth_repository import AuthRepository
from src.repositories.user_repository import UserRepository
from src.schemas.auth_schema import RegisterSchema, LoginSchema, LoginResponseSchema


class AuthService:
    def __init__(self, repository: AuthRepository, user_repository: UserRepository):
        self._repository = repository
        self._user_repository = user_repository

    def register(self, schema: RegisterSchema):
        user_data = schema.model_dump()
        if "password" in user_data:
            user_data["password"] = PasswordHasher.hash(user_data["password"])
        data = UserModel(**user_data)
        conflicts = {}
        if self._user_repository.get_user_by_email(data.email):
            conflicts["email"] = data.email
        if self._user_repository.get_user_by_username(data.username):
            conflicts["username"] = data.username
        if conflicts:
            raise ConflictError(conflicts=conflicts)
        return self._repository.register(data)

    def login(self, schema: LoginSchema):
        error_msg = "Tài khoản hoặc mật khẩu không chính xác"
        user_exist = self._user_repository.get_user_by_username(schema.username)
        if not user_exist:
            raise UnauthorizedError(error_msg)
        is_valid_pass = PasswordHasher.verify(schema.password, user_exist.password)
        if not is_valid_pass:
            raise UnauthorizedError(error_msg)
        access_token = TokenConfig.create_access_token(user_id=user_exist.id, username=user_exist.username)
        refresh_token, expire_time = TokenConfig.create_refresh_token(user_id=user_exist.id)
        new_token_data = TokenModel(
            user_id=user_exist.id,
            refresh_token=refresh_token,
            expires_at=expire_time,
            is_revoked=False
        )
        self._repository.save_refresh_token(new_token_data)
        return LoginResponseSchema(access_token=access_token, refresh_token=refresh_token)
