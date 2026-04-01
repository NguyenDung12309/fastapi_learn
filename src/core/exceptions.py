class AppError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class NotFoundError(AppError):
    def __init__(self):
        super().__init__(
            message=f"id not found",
            status_code=404
        )


class ValidationError(AppError):
    def __init__(self, message: str):
        super().__init__(message=message, status_code=422)


class ConflictError(AppError):
    def __init__(self, identifier: str):
        super().__init__(message=f"'{identifier}' is existed", status_code=409)
