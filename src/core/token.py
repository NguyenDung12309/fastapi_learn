from datetime import timedelta, datetime, timezone
from uuid import UUID

import jwt

from src.core.config import Config
from src.core.exceptions import UnauthorizedError


class TokenConfig:
    @staticmethod
    def _generate_token(data: dict, expires_delta: timedelta) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, Config.SECRET_KEY, algorithm=Config.ALGORITHM)

    @classmethod
    def create_access_token(cls, user_id: UUID, username: str) -> str:
        payload = {
            "id": str(user_id),
            "username": username,
        }
        return cls._generate_token(
            payload,
            timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_M)
        )

    @classmethod
    def create_refresh_token(cls, user_id: UUID) -> tuple[str, datetime]:
        payload = {
            "id": str(user_id),
        }
        expires_delta = datetime.now(timezone.utc) + timedelta(days=Config.REFRESH_TOKEN_EXPIRE_D)
        token = cls._generate_token(
            payload,
            timedelta(days=Config.REFRESH_TOKEN_EXPIRE_D)
        )
        return token, expires_delta

    @staticmethod
    def decode_token(token: str) -> dict:
        try:
            payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise UnauthorizedError("Token đã hết hạn")
        except jwt.InvalidTokenError:
            raise UnauthorizedError("Token không hợp lệ")
