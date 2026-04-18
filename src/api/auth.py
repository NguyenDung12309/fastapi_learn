from fastapi import APIRouter, Depends, BackgroundTasks
from sqlmodel import Session

from src.core.dependency import access_token_bear_depend
from src.core.redis_store import redis_store
from src.db.main import db_manager
from src.models import UserModel
from src.repositories.auth_repository import AuthRepository
from src.repositories.user_repository import UserRepository
from src.schemas.auth_schema import RegisterSchema, LoginSchema, LoginResponseSchema, AccessTokenRequestSchema, \
    AccessTokenResponseSchema, LogoutRequestSchema, AccessTokenDataSchema
from src.services.auth_service import AuthService

auth_router = APIRouter()


def get_auth_service(session: Session = Depends(db_manager.get_db)) -> AuthService:
    repository = AuthRepository(session)
    user_repository = UserRepository(session)
    return AuthService(repository, user_repository)


@auth_router.post("/register", response_model=UserModel)
def register(payload: RegisterSchema, background_tasks: BackgroundTasks,
             service: AuthService = Depends(get_auth_service)):
    return service.register(payload, background_tasks=background_tasks)


@auth_router.post("/login", response_model=LoginResponseSchema)
def login(payload: LoginSchema, service: AuthService = Depends(get_auth_service)):
    return service.login(payload)


@auth_router.post("/refresh", response_model=AccessTokenResponseSchema)
def refresh_token(payload: AccessTokenRequestSchema, service: AuthService = Depends(get_auth_service)):
    return service.get_access_token(payload)


@auth_router.post("/logout")
def logout(payload: LogoutRequestSchema, credentials: AccessTokenDataSchema = Depends(access_token_bear_depend),
           service: AuthService = Depends(get_auth_service)):
    redis_store.add_jti_to_blocklist(jti=credentials.jti, expires_in=credentials.exp)
    service.revoke_refresh_token(payload.refresh_token)
