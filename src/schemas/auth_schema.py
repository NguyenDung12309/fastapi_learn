from enum import Enum
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
    refresh_token: str


class TokenType(str, Enum):
    ACCESS = "access_token"
    REFRESH = "refresh_token"


class TokenDataSchema(BaseModel):
    id: str
    type: TokenType
    exp: Optional[int] = None


class AccessTokenDataSchema(TokenDataSchema):
    jti: str
    username: str


class RefreshTokenDataSchema(TokenDataSchema):
    username: str


class AccessTokenRequestSchema(BaseModel):
    refresh_token: str


class AccessTokenResponseSchema(BaseModel):
    access_token: str


class LogoutRequestSchema(BaseModel):
    refresh_token: str
