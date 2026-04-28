from src.common.enum_common import UserRole, PermissionKey

ROLE_PERMISSIONS = {
    UserRole.GUEST: [],
    UserRole.USER: [],
    UserRole.ADMIN: [p for p in PermissionKey]
}
