from fastapi import APIRouter, Depends
from sqlmodel import Session

from src.db.main import db_manager
from src.models import UserModel
from src.repositories.user_repository import UserRepository
from src.schemas.user_schema import UserCreateSchema
from src.services.user_service import UserService

auth_router = APIRouter()


def get_user_service(session: Session = Depends(db_manager.get_db)) -> UserService:
    repository = UserRepository(session)
    return UserService(repository)


@auth_router.post("/register", response_model=UserModel)
def create_user(payload: UserCreateSchema, service: UserService = Depends(get_user_service)):
    return service.create(payload)
