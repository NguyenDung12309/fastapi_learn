from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


class TokenType(str, Enum):
    ACCESS = "access_token"
    REFRESH = "refresh_token"
    RESET_PASSWORD = "reset_password"


class PermissionKey(str, Enum):
    CREATE_CATEGORY = "create__category"
    UPDATE_CATEGORY = "update__category"
