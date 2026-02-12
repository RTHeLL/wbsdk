"""Тесты OrdersDBSAPI."""

import pytest
import respx

from wbsdk import WBClient
from wbsdk.schemas.orders_dbs import OrdersListResponse, OrdersNewResponse

BASE_URL = "https://marketplace-api.wildberries.ru"


@pytest.fixture
def client() -> WBClient:
    return WBClient(token="test-token")


@respx.mock
def test_get_new_orders(client: WBClient) -> None:
    """Тест get_new_orders."""
    respx.get(f"{BASE_URL}/api/v3/dbs/orders/new").mock(
        return_value=respx.MockResponse(200, json={"orders": []})
    )
    result = client.orders_dbs.get_new_orders()
    assert isinstance(result, OrdersNewResponse)
    assert result.orders == []


@respx.mock
def test_get_orders(client: WBClient) -> None:
    """Тест get_orders."""
    respx.get(f"{BASE_URL}/api/v3/dbs/orders").mock(
        return_value=respx.MockResponse(200, json={"orders": [], "next": 0})
    )
    result = client.orders_dbs.get_orders(
        date_from=1704067200, date_to=1706745599
    )
    assert isinstance(result, OrdersListResponse)
    assert result.orders == []


@respx.mock
def test_cancel_order(client: WBClient) -> None:
    """Тест cancel_order."""
    respx.patch(f"{BASE_URL}/api/v3/dbs/orders/1/cancel").mock(
        return_value=respx.MockResponse(204)
    )
    client.orders_dbs.cancel_order(order_id=1)


@respx.mock
def test_get_orders_status_info(client: WBClient) -> None:
    """Тест get_orders_status_info (marketplace)."""
    respx.post(f"{BASE_URL}/api/marketplace/v3/dbs/orders/status/info").mock(
        return_value=respx.MockResponse(200, json={"orders": []})
    )
    result = client.orders_dbs.get_orders_status_info(order_ids=[1])
    assert result is not None
