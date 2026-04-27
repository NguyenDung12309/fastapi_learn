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
    VIEW_CATEGORY_LIST = "view__category_list"
