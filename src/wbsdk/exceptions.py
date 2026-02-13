"""Исключения WB API SDK."""


class WBAPIError(Exception):
    """Базовое исключение для ошибок WB API."""

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        response_data: dict | None = None,
    ):
        self.message = message
        self.status_code = status_code
        self.response_data = response_data or {}
        super().__init__(self.message)

    def __str__(self) -> str:
        parts = [self.message]
        if self.status_code is not None:
            parts.append(f"HTTP {self.status_code}")
        if self.response_data:
            error_text = self.response_data.get("errorText") or self.response_data.get("detail")
            if error_text:
                parts.append(f": {error_text}")
        return " ".join(parts)


class WBAuthError(WBAPIError):
    """Ошибка авторизации (401, 403)."""

    pass


class WBRateLimitError(WBAPIError):
    """Превышен лимит запросов (429)."""

    pass


class WBValidationError(WBAPIError):
    """Ошибка валидации запроса (400, 422)."""

    pass


class WBConflictError(WBAPIError):
    """Конфликт при выполнении операции (409)."""

    pass


class WBNotFoundError(WBAPIError):
    """Ресурс не найден (404)."""

    pass


def raise_for_status(status_code: int, response_data: dict, response_text: str = "") -> None:
    """Преобразует HTTP-ошибку в соответствующее исключение."""
    error_classes = {
        400: WBValidationError,
        401: WBAuthError,
        403: WBAuthError,
        404: WBNotFoundError,
        409: WBConflictError,
        422: WBValidationError,
        429: WBRateLimitError,
    }
    error_class = error_classes.get(status_code, WBAPIError)
    raise error_class(
        message="API request failed",
        status_code=status_code,
        response_data=response_data or {"detail": response_text},
    )
