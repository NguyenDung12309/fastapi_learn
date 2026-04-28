from typing import Sequence
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlmodel import Session

from src.core.dependency import access_token_bear_depend
from src.db.main import db_manager
from src.models import UserModel
from src.repositories.user_repository import UserRepository
from src.schemas.auth_schema import AccessTokenDataSchema, ChangePasswordRequestSchema
from src.schemas.user_schema import GetMeResponseSchema
from src.services.user_service import UserService

user_router = APIRouter()


def get_user_service(session: Session = Depends(db_manager.get_db)) -> UserService:
    repository = UserRepository(session)
    return UserService(repository)


@user_router.get("/", dependencies=[Depends(access_token_bear_depend)], response_model=Sequence[UserModel])
def get_user_list(service: UserService = Depends(get_user_service)):
    return service.get_all()


@user_router.get("/me", response_model=GetMeResponseSchema)
def get_current_user_info(
        token_data: AccessTokenDataSchema = Depends(access_token_bear_depend),
        service: UserService = Depends(get_user_service)
):
    return service.get_me(UUID(token_data.id))


@user_router.patch("/change-password")
def change_password(payload: ChangePasswordRequestSchema,
                    token_data: AccessTokenDataSchema = Depends(access_token_bear_depend),
                    service: UserService = Depends(get_user_service)):
    return service.update_password(user_id=UUID(token_data.id), schema=payload)
