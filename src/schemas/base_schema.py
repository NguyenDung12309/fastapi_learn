from datetime import datetime
from typing import Generic, TypeVar, Optional
from uuid import UUID

from pydantic import BaseModel

T = TypeVar("T")


class BaseCreateSchema(BaseModel, Generic[T]):
    id: Optional[UUID]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
