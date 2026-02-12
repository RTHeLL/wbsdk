"""Тесты OrdersFBWAPI."""

import pytest
import respx

from wbsdk import WBClient

BASE_URL = "https://supplies-api.wildberries.ru"


@pytest.fixture
def client() -> WBClient:
    return WBClient(token="test-token")


@respx.mock
def test_get_warehouses(client: WBClient) -> None:
    """Тест get_warehouses."""
    respx.get(f"{BASE_URL}/api/v1/warehouses").mock(
        return_value=respx.MockResponse(200, json=[])
    )
    result = client.orders_fbw.get_warehouses()
    assert result == []


@respx.mock
def test_get_transit_tariffs(client: WBClient) -> None:
    """Тест get_transit_tariffs."""
    respx.get(f"{BASE_URL}/api/v1/transit-tariffs").mock(
        return_value=respx.MockResponse(200, json=[])
    )
    result = client.orders_fbw.get_transit_tariffs()
    assert result == []


@respx.mock
def test_get_supplies(client: WBClient) -> None:
    """Тест get_supplies."""
    respx.post(f"{BASE_URL}/api/v1/supplies").mock(
        return_value=respx.MockResponse(200, json=[])
    )
    result = client.orders_fbw.get_supplies(payload={"dates": []})
    assert result == []


@respx.mock
def test_get_supply_details(client: WBClient) -> None:
    """Тест get_supply_details."""
    respx.get(f"{BASE_URL}/api/v1/supplies/123").mock(
        return_value=respx.MockResponse(200, json={"supplyID": 123})
    )
    result = client.orders_fbw.get_supply_details(supply_id=123)
    assert result is not None
