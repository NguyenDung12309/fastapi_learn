from typing import Optional

from pydantic import BaseModel, Field, EmailStr


class AuthBaseSchema(BaseModel):
    username: str = Field(..., min_length=1, max_length=100)
    email: EmailStr = Field(..., min_length=1, max_length=100)
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=5, max_length=50)
    is_verified: Optional[bool] = Field(default=False)


class RegisterSchema(AuthBaseSchema):
    pass


class LoginSchema(BaseModel):
    username: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=1, max_length=100)


class LoginResponseSchema(BaseModel):
    access_token: str
