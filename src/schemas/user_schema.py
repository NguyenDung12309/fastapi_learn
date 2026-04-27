from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, Field, EmailStr

from src.common.enum_common import PermissionKey


class UserBaseSchema(BaseModel):
    username: str = Field(..., min_length=1, max_length=100)
    email: EmailStr = Field(..., min_length=1, max_length=100)
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    is_verified: Optional[bool] = Field(default=False)


class UserCreateSchema(UserBaseSchema):
    password: str = Field(..., min_length=5, max_length=50)
    pass


class UserUpdateSchema(UserBaseSchema):
    pass


class UserLoginSchema(BaseModel):
    username: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=1, max_length=100)


class UserLoginResponseSchema(BaseModel):
    access_token: str
    refresh_token: str


class GetMeResponseSchema(UserBaseSchema):
    id: UUID
    permissions: List[PermissionKey] = Field(default_factory=list)


class ForgotPasswordRequestSchema(BaseModel):
    email: EmailStr


class ResetPasswordRequestSchema(BaseModel):
    token: str
    new_password: str = Field(..., min_length=5, max_length=50)
