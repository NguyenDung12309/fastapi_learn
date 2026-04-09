from fastapi import APIRouter, Depends
from sqlmodel import Session

from src.db.main import db_manager
from src.models import UserModel
from src.repositories.auth_repository import AuthRepository
from src.repositories.user_repository import UserRepository
from src.schemas.auth_schema import RegisterSchema, LoginSchema, LoginResponseSchema
from src.services.auth_service import AuthService

auth_router = APIRouter()


def get_auth_service(session: Session = Depends(db_manager.get_db)) -> AuthService:
    repository = AuthRepository(session)
    user_repository = UserRepository(session)
    return AuthService(repository, user_repository)


@auth_router.post("/register", response_model=UserModel)
def register(payload: RegisterSchema, service: AuthService = Depends(get_auth_service)):
    return service.register(payload)


@auth_router.post("/login", response_model=LoginResponseSchema)
def login(payload: LoginSchema, service: AuthService = Depends(get_auth_service)):
    return service.login(payload)
