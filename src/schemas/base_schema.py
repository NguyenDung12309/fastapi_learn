from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class BaseCreateSchema(BaseModel, Generic[T]):
    pass
