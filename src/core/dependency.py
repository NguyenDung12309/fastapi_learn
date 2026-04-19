from typing import List

from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.requests import Request

from src.common.enum_common import UserRole
from src.core.exceptions import ForbiddenError
from src.core.token import token_config
from src.schemas.auth_schema import AccessTokenDataSchema


class TokenBearerAuthentication(HTTPBearer):
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)

        return creds


class AccessTokenBearerAuthentication(TokenBearerAuthentication):
    async def __call__(self, request: Request) -> AccessTokenDataSchema:
        creds = await super().__call__(request)
        token_data = token_config.decode_token_access(creds.credentials)
        return token_data


access_token_bear_depend = AccessTokenBearerAuthentication()


class RoleChecker:

    def __init__(self, allowed_roles: List[UserRole]):
        self.allowed_roles = allowed_roles

    def __call__(self, token_data: AccessTokenDataSchema = Depends(access_token_bear_depend)):
        user_role = getattr(token_data, "role", UserRole.USER)

        if user_role not in self.allowed_roles:
            raise ForbiddenError(f"Quyền {user_role} không thể thực hiện hành động này.")

        return token_data


allow_admin = RoleChecker([UserRole.ADMIN])
allow_moderator_admin = RoleChecker([UserRole.ADMIN, UserRole.USER])
