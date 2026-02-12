"""Тесты OrdersDBWAPI."""

import pytest
import respx

from wbsdk import WBClient
from wbsdk.schemas.orders_dbw import OrdersListResponse, OrdersNewResponse

BASE_URL = "https://marketplace-api.wildberries.ru"


@pytest.fixture
def client() -> WBClient:
    return WBClient(token="test-token")


@respx.mock
def test_get_new_orders(client: WBClient) -> None:
    """Тест get_new_orders."""
    respx.get(f"{BASE_URL}/api/v3/dbw/orders/new").mock(
        return_value=respx.MockResponse(200, json={"orders": []})
    )
    result = client.orders_dbw.get_new_orders()
    assert isinstance(result, OrdersNewResponse)
    assert result.orders == []


@respx.mock
def test_get_orders(client: WBClient) -> None:
    """Тест get_orders."""
    respx.get(f"{BASE_URL}/api/v3/dbw/orders").mock(
        return_value=respx.MockResponse(200, json={"orders": [], "next": 0})
    )
    result = client.orders_dbw.get_orders(
        date_from=1704067200, date_to=1706745599
    )
    assert isinstance(result, OrdersListResponse)
    assert result.orders == []


@respx.mock
def test_get_orders_delivery_date(client: WBClient) -> None:
    """Тест get_orders_delivery_date."""
    respx.post(f"{BASE_URL}/api/v3/dbw/orders/delivery-date").mock(
        return_value=respx.MockResponse(200, json={})
    )
    result = client.orders_dbw.get_orders_delivery_date(payload={"orders": [1]})
    assert result is not None


@respx.mock
def test_confirm_order(client: WBClient) -> None:
    """Тест confirm_order."""
    respx.patch(f"{BASE_URL}/api/v3/dbw/orders/1/confirm").mock(
        return_value=respx.MockResponse(204)
    )
    client.orders_dbw.confirm_order(order_id=1)


@respx.mock
def test_cancel_order(client: WBClient) -> None:
    """Тест cancel_order."""
    respx.patch(f"{BASE_URL}/api/v3/dbw/orders/1/cancel").mock(
        return_value=respx.MockResponse(204)
    )
    client.orders_dbw.cancel_order(order_id=1)


@respx.mock
def test_get_order_meta(client: WBClient) -> None:
    """Тест get_order_meta."""
    respx.get(f"{BASE_URL}/api/v3/dbw/orders/1/meta").mock(
        return_value=respx.MockResponse(200, json={"imei": [], "uin": []})
    )
    result = client.orders_dbw.get_order_meta(order_id=1)
    assert "imei" in result or result is not None
