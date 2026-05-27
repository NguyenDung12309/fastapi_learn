from typing import Sequence

from fastapi import APIRouter, Depends
from sqlmodel import Session

from src.common.enum_common import PermissionKey
from src.core.dependency import access_token_bear_depend, PermissionChecker
from src.db.main import db_manager
from src.models import AuthorModel
from src.repositories.author_repository import AuthorRepository
from src.schemas.author_schema import CreateOrGetAuthorSchema
from src.services.author_service import AuthorService

author_router = APIRouter()


def get_author_service(session: Session = Depends(db_manager.get_db)) -> AuthorService:
    repository = AuthorRepository(session)
    return AuthorService(repository)


@author_router.get("/", response_model=Sequence[AuthorModel])
def list_author(service: AuthorService = Depends(get_author_service)):
    return service.get_all()


@author_router.post("/", response_model=AuthorModel, dependencies=[Depends(access_token_bear_depend),
                                                                   Depends(PermissionChecker(
                                                                       PermissionKey.CREATE_CATEGORY))])
def create_author(payload: CreateOrGetAuthorSchema, service: AuthorService = Depends(get_author_service)):
    return service.create_or_get_author(payload)
