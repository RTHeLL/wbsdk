"""Тесты исключений."""

import pytest

from wbsdk.exceptions import (
    WBAPIError,
    WBAuthError,
    WBConflictError,
    WBNotFoundError,
    WBRateLimitError,
    WBValidationError,
    raise_for_status,
)


def test_wb_api_error_str() -> None:
    """WBAPIError формирует строку с деталями."""
    err = WBAPIError("Test", status_code=400, response_data={"errorText": "Bad"})
    assert "Test" in str(err)
    assert err.status_code == 400


def test_raise_for_status_401() -> None:
    """raise_for_status создаёт WBAuthError для 401."""
    with pytest.raises(WBAuthError):
        raise_for_status(401, {"detail": "Unauthorized"})


def test_raise_for_status_429() -> None:
    """raise_for_status создаёт WBRateLimitError для 429."""
    with pytest.raises(WBRateLimitError):
        raise_for_status(429, {})


def test_raise_for_status_409() -> None:
    """raise_for_status создаёт WBConflictError для 409."""
    with pytest.raises(WBConflictError):
        raise_for_status(409, {})


def test_raise_for_status_404() -> None:
    """raise_for_status создаёт WBNotFoundError для 404."""
    with pytest.raises(WBNotFoundError):
        raise_for_status(404, {})


def test_raise_for_status_400() -> None:
    """raise_for_status создаёт WBValidationError для 400."""
    with pytest.raises(WBValidationError):
        raise_for_status(400, {})
