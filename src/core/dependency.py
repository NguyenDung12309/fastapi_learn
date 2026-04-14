from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.requests import Request

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
