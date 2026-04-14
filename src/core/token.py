from datetime import timedelta, datetime, timezone
from typing import TypeVar, Type
from uuid import UUID, uuid4

import jwt
from pydantic import ValidationError

from src.core.config import Config
from src.core.exceptions import UnauthorizedError, ForbiddenError
from src.core.redis_store import redis_store
from src.schemas.auth_schema import TokenDataSchema, AccessTokenDataSchema, TokenType, RefreshTokenDataSchema

T = TypeVar("T", bound=TokenDataSchema)


class TokenConfig:
    @staticmethod
    def _generate_token(data: dict, expires_delta: timedelta) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, Config.SECRET_KEY, algorithm=Config.ALGORITHM)

    @classmethod
    def create_access_token(cls, user_id: UUID, username: str) -> str:
        payload = AccessTokenDataSchema(
            id=str(user_id),
            username=username,
            type=TokenType.ACCESS,
            jti=str(uuid4())
        )
        return cls._generate_token(
            payload.model_dump(),
            timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_M)
        )

    @classmethod
    def create_refresh_token(cls, user_id: UUID, username: str) -> tuple[str, datetime]:
        payload = RefreshTokenDataSchema(
            id=str(user_id),
            username=username,
            type=TokenType.REFRESH,
        )
        expires_delta = datetime.now(timezone.utc) + timedelta(days=Config.REFRESH_TOKEN_EXPIRE_D)
        token = cls._generate_token(
            payload.model_dump(),
            timedelta(days=Config.REFRESH_TOKEN_EXPIRE_D)
        )
        return token, expires_delta

    @staticmethod
    def _decode_base(token: str, schema_type: Type[T]) -> T:
        try:
            payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
            return schema_type.model_validate(payload)
        except jwt.ExpiredSignatureError:
            raise UnauthorizedError("Token đã hết hạn")
        except (jwt.InvalidTokenError, ValidationError):
            raise UnauthorizedError("Token không hợp lệ")

    @classmethod
    def decode_token_access(cls, token: str) -> AccessTokenDataSchema:
        token_data = cls._decode_base(token, AccessTokenDataSchema)
        if not token_data or token_data.type != TokenType.ACCESS:
            raise ForbiddenError("Token không phải là Access Token")
        jti = token_data.jti
        is_exist = redis_store.token_in_blocklist(jti=jti)
        if is_exist:
            raise UnauthorizedError("Token đã bị vô hiệu hóa")
        return token_data

    @classmethod
    def decode_token_refresh(cls, token: str) -> RefreshTokenDataSchema:
        token_data = cls._decode_base(token, RefreshTokenDataSchema)
        if not token_data or token_data.type != TokenType.REFRESH:
            raise ForbiddenError("Token không phải là Refresh Token")
        return token_data


token_config = TokenConfig()
