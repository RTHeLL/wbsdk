"""Тесты UserManagementAPI."""

import pytest
import respx

from wbsdk import WBClient
from wbsdk.schemas.user_management import CreateInviteResponse, GetUsersResponse

BASE_URL = "https://user-management-api.wildberries.ru"


@pytest.fixture
def client() -> WBClient:
    return WBClient(token="test-token")


@respx.mock
def test_create_invite(client: WBClient) -> None:
    """Тест create_invite."""
    respx.post(f"{BASE_URL}/api/v1/invite").mock(
        return_value=respx.MockResponse(
            200,
            json={
                "inviteID": "uuid-123",
                "expiredAt": "2025-12-01T00:00:00Z",
                "isSuccess": True,
                "inviteUrl": "https://seller.wildberries.ru/invite/123",
            },
        )
    )
    result = client.user_management.create_invite(phone_number="79991234567")
    assert isinstance(result, CreateInviteResponse)
    assert result.is_success is True
    assert result.invite_id == "uuid-123"


@respx.mock
def test_get_users(client: WBClient) -> None:
    """Тест get_users."""
    respx.get(f"{BASE_URL}/api/v1/users").mock(
        return_value=respx.MockResponse(
            200,
            json={"total": 1, "countInResponse": 1, "users": []},
        )
    )
    result = client.user_management.get_users()
    assert isinstance(result, GetUsersResponse)
    assert result.total == 1
    assert result.users == []


@respx.mock
def test_update_users_access(client: WBClient) -> None:
    """Тест update_users_access."""
    respx.put(f"{BASE_URL}/api/v1/users/access").mock(
        return_value=respx.MockResponse(200)
    )
    client.user_management.update_users_access(
        users_accesses=[{"userId": 1, "access": [{"code": "balance", "disabled": False}]}]
    )


@respx.mock
def test_delete_user(client: WBClient) -> None:
    """Тест delete_user."""
    respx.delete(f"{BASE_URL}/api/v1/user").mock(
        return_value=respx.MockResponse(200)
    )
    client.user_management.delete_user(user_id=123)
