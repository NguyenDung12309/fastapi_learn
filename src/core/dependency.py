from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.requests import Request


class BearerAuthentication(HTTPBearer):
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)
        print(creds.scheme)
        print(creds.credentials)
        return creds
