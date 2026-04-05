from typing import Sequence

from fastapi import APIRouter, Depends
from sqlmodel import Session

from src.db.main import db_manager
from src.models import UserModel
from src.repositories.user_repository import UserRepository
from src.services.user_service import UserService

user_router = APIRouter()


def get_user_service(session: Session = Depends(db_manager.get_db)) -> UserService:
    repository = UserRepository(session)
    return UserService(repository)


@user_router.get("/", response_model=Sequence[UserModel])
def get_user_list(service: UserService = Depends(get_user_service)):
    return service.get_all()
