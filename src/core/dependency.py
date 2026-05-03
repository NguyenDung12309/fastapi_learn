from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.requests import Request

from src.common.enum_common import PermissionKey
from src.common.matrix_permission import ROLE_PERMISSIONS
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
        print("111111111111111111")
        creds = await super().__call__(request)
        token_data = token_config.decode_token_access(creds.credentials)
        request.state.user = token_data
        return token_data


access_token_bear_depend = AccessTokenBearerAuthentication()


class PermissionChecker:
    def __init__(self, required_permission: PermissionKey):
        self.required_permission = required_permission

    def __call__(self, request: Request):
        token_data: AccessTokenDataSchema = getattr(request.state, "user", None)
        user_role = token_data.role

        user_permissions = ROLE_PERMISSIONS.get(user_role, [])

        if self.required_permission not in user_permissions:
            raise ForbiddenError(f"Yêu cầu quyền: {self.required_permission}")

        return True
