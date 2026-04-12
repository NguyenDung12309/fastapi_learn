from typing import Any, Dict, Optional, Union


class AppError(Exception):
    def __init__(
            self,
            message: str,
            status_code: int = 400,
            errors: Optional[Union[Dict[str, Any], list]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.errors = errors
        super().__init__(self.message)

    def to_response(self):
        payload = {
            "status": "error",
            "message": self.message,
            "code": self.status_code
        }
        if self.errors is not None:
            payload["errors"] = self.errors
        return payload


class ValidationError(AppError):
    def __init__(self, field_errors: Dict[str, str]):
        super().__init__(
            message="Dữ liệu đầu vào không hợp lệ",
            status_code=422,
            errors=field_errors
        )


class ConflictError(AppError):
    def __init__(self, conflicts: Dict[str, Any]):
        detail_errors = {
            field: f"Giá trị '{value}' đã tồn tại trong hệ thống"
            for field, value in conflicts.items()
        }
        super().__init__(
            message="Xung đột dữ liệu",
            status_code=409,
            errors=detail_errors
        )


class NotFoundError(AppError):
    def __init__(self, resource_details: Dict[str, Any]):
        detail_errors = {
            field: f"Không tìm thấy bản ghi với {field} = {value}"
            for field, value in resource_details.items()
        }
        super().__init__(
            message="Không tìm thấy tài nguyên",
            status_code=404,
            errors=detail_errors
        )


class UnauthorizedError(AppError):
    def __init__(self, message: str = "Không có quyền truy cập"):
        super().__init__(
            message=message,
            status_code=401
        )


class ForbiddenError(AppError):
    def __init__(self, message: str = "Bạn không có quyền thực hiện hành động này"):
        super().__init__(
            message=message,
            status_code=403
        )
