"""Тесты ClickCollectAPI."""

import pytest
import respx

from wbsdk import WBClient
from wbsdk.schemas.click_collect import OrdersListResponse, OrdersNewResponse

BASE_URL = "https://marketplace-api.wildberries.ru"


@pytest.fixture
def client() -> WBClient:
    return WBClient(token="test-token")


@respx.mock
def test_get_new_orders(client: WBClient) -> None:
    """Тест get_new_orders."""
    respx.get(f"{BASE_URL}/api/v3/click-collect/orders/new").mock(
        return_value=respx.MockResponse(200, json={"orders": []})
    )
    result = client.click_collect.get_new_orders()
    assert isinstance(result, OrdersNewResponse)
    assert result.orders == []


@respx.mock
def test_confirm_order(client: WBClient) -> None:
    """Тест confirm_order."""
    respx.patch(f"{BASE_URL}/api/v3/click-collect/orders/1/confirm").mock(
        return_value=respx.MockResponse(204)
    )
    client.click_collect.confirm_order(order_id=1)


@respx.mock
def test_get_orders(client: WBClient) -> None:
    """Тест get_orders."""
    respx.get(f"{BASE_URL}/api/v3/click-collect/orders").mock(
        return_value=respx.MockResponse(200, json={"orders": [], "next": 0})
    )
    result = client.click_collect.get_orders(
        date_from=1704067200, date_to=1706745599
    )
    assert isinstance(result, OrdersListResponse)
    assert result.orders == []


@respx.mock
def test_get_orders_client(client: WBClient) -> None:
    """Тест get_orders_client."""
    respx.post(f"{BASE_URL}/api/v3/click-collect/orders/client").mock(
        return_value=respx.MockResponse(200, json={"orders": []})
    )
    result = client.click_collect.get_orders_client(order_ids=[1])
    assert result is not None
