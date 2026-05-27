from src.common.enum_common import UserRole, PermissionKey

ROLE_PERMISSIONS = {
    UserRole.GUEST: [],
    UserRole.USER: [PermissionKey.UPLOAD_MEDIA, PermissionKey.UPLOAD_BOOK],
    UserRole.ADMIN: [p for p in PermissionKey]
}
