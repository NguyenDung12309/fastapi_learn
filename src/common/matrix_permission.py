from src.common.enum_common import UserRole, PermissionKey

ROLE_PERMISSIONS = {
    UserRole.GUEST: [
        PermissionKey.VIEW_CATEGORY_LIST
    ],
    UserRole.USER: [
        PermissionKey.VIEW_CATEGORY_LIST,
    ],
    UserRole.ADMIN: [p for p in PermissionKey]
}
