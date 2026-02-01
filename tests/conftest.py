"""Pytest fixtures для тестов WB SDK."""

import pytest

from wbsdk import WBClient


@pytest.fixture
def token() -> str:
    """Тестовый токен."""
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test"


@pytest.fixture
def client(token: str) -> WBClient:
    """Клиент WB с тестовым токеном."""
    return WBClient(token=token)
