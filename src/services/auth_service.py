from datetime import datetime, timezone

from fastapi import BackgroundTasks

from src.core.exceptions import ConflictError, UnauthorizedError
from src.core.security import password_hasher
from src.core.token import token_config
from src.models import UserModel
from src.models.token_model import TokenModel
from src.repositories.auth_repository import AuthRepository
from src.repositories.user_repository import UserRepository
from src.schemas.auth_schema import RegisterSchema, LoginSchema, LoginResponseSchema, AccessTokenRequestSchema, \
    AccessTokenResponseSchema, CreateAccessTokenSchema
from src.services.email_service import EmailService


class AuthService:
    def __init__(self, repository: AuthRepository, user_repository: UserRepository):
        self._repository = repository
        self._user_repository = user_repository

    def register(self, schema: RegisterSchema, background_tasks: BackgroundTasks):
        user_data = schema.model_dump()
        if "password" in user_data:
            user_data["password"] = password_hasher.hash(user_data["password"])
        data = UserModel(**user_data)
        conflicts = {}
        if self._user_repository.get_user_by_email(data.email):
            conflicts["email"] = data.email
        if self._user_repository.get_user_by_username(data.username):
            conflicts["username"] = data.username
        if conflicts:
            raise ConflictError(conflicts=conflicts)
        new_user = self._repository.register(data)
        background_tasks.add_task(
            EmailService.send_registration_email,
            to_email=new_user.email,
            username=new_user.username
        )
        return new_user

    def login(self, schema: LoginSchema):
        error_msg = "Tài khoản hoặc mật khẩu không chính xác"
        user_exist = self._user_repository.get_user_by_username(schema.username)
        if not user_exist:
            raise UnauthorizedError(error_msg)
        is_valid_pass = password_hasher.verify(schema.password, user_exist.password)
        if not is_valid_pass:
            raise UnauthorizedError(error_msg)
        user_data = CreateAccessTokenSchema(
            username=user_exist.username,
            id=user_exist.id,
            role=user_exist.role
        )
        access_token = token_config.create_access_token(user_data)
        refresh_token, expire_time = token_config.create_refresh_token(user_id=user_exist.id,
                                                                       username=user_exist.username)
        new_token_data = TokenModel(
            user_id=user_exist.id,
            refresh_token=refresh_token,
            expires_at=expire_time,
            is_revoked=False
        )
        self._repository.save_refresh_token(new_token_data)
        return LoginResponseSchema(access_token=access_token, refresh_token=refresh_token)

    def revoke_refresh_token(self, refresh_token: str):
        self.verify_refresh_token(refresh_token)
        self._repository.revoke_refresh_token(refresh_token)

    def verify_refresh_token(self, refresh_token: str):
        refresh_token_record = self._repository.get_refresh_token(refresh_token)
        if not refresh_token_record or refresh_token_record.is_revoked or refresh_token_record.expires_at < datetime.now(
                timezone.utc):
            raise UnauthorizedError("Refresh Token không hợp lệ hoặc đã hết hạn")
        return refresh_token_record

    def get_access_token(self, schema: AccessTokenRequestSchema):
        refresh_token_record = self.verify_refresh_token(schema.refresh_token)
        decode_token = token_config.decode_token_refresh(refresh_token_record.refresh_token)
        user_info = self._user_repository.get_by_id(decode_token.id)
        new_access_token = token_config.create_access_token(user_info)
        self.revoke_refresh_token(schema.refresh_token)
        return AccessTokenResponseSchema(
            access_token=new_access_token,
        )
