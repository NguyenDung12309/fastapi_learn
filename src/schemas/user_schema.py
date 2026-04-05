from typing import Optional

from pydantic import BaseModel, Field


class UserBaseSchema(BaseModel):
    username: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., min_length=1, max_length=100)
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=5, max_length=50)
    is_verified: Optional[bool] = Field(default=False)


class UserCreateSchema(UserBaseSchema):
    pass


class UserUpdateSchema(UserBaseSchema):
    pass
