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


@respx.mock
def test_delete_order_meta(client: WBClient) -> None:
    """Тест delete_order_meta — удаление метаданных по ключу."""
    route = respx.delete(
        f"{BASE_URL}/api/v3/click-collect/orders/123/meta"
    ).mock(return_value=respx.MockResponse(204))
    client.click_collect.delete_order_meta(order_id=123, key="imei")
    assert route.called
    assert "key=imei" in str(route.calls.last.request.url)


@respx.mock
def test_delete_order_meta_without_key(client: WBClient) -> None:
    """Тест delete_order_meta без key."""
    route = respx.delete(
        f"{BASE_URL}/api/v3/click-collect/orders/456/meta"
    ).mock(return_value=respx.MockResponse(204))
    client.click_collect.delete_order_meta(order_id=456)
    assert route.called
