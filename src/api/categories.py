from typing import Sequence
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlmodel import Session

from src.db.main import db_manager
from src.models.categories_model import CategoryModel
from src.repositories.categories_repository import CategoryRepository
from src.schemas.category_schema import CategoryCreateSchema, CategoryUpdateSchema
from src.services.categories_service import CategoryService

category_router = APIRouter()


def get_category_service(session: Session = Depends(db_manager.get_db)) -> CategoryService:
    repository = CategoryRepository(session)
    return CategoryService(repository)


@category_router.post("/", response_model=CategoryModel)
def create_category(payload: CategoryCreateSchema, service: CategoryService = Depends(get_category_service)):
    return service.create(payload)


@category_router.get("/", response_model=Sequence[CategoryModel])
def list_category(service: CategoryService = Depends(get_category_service)):
    return service.get_all()


@category_router.get("/{uid}", response_model=CategoryModel)
def category_detail(uid: UUID, service: CategoryService = Depends(get_category_service)):
    return service.get_by_id(uid)


@category_router.patch("/{uid}", response_model=CategoryModel)
def category_update(uid: UUID, payload: CategoryUpdateSchema, service: CategoryService = Depends(get_category_service)):
    return service.update(uid, payload)
