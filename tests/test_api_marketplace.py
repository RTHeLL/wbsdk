"""Тесты MarketplaceAPI."""

import pytest
import respx

from wbsdk import WBClient


@pytest.fixture
def client() -> WBClient:
    return WBClient(token="test-token")


@respx.mock
def test_get_new_orders(client: WBClient) -> None:
    """Тест get_new_orders."""
    respx.get("https://marketplace-api.wildberries.ru/api/v3/orders/new").mock(
        return_value=respx.MockResponse(200, json={"orders": []})
    )
    result = client.marketplace.get_new_orders()
    assert "orders" in result
    assert result["orders"] == []


@respx.mock
def test_create_supply(client: WBClient) -> None:
    """Тест create_supply."""
    respx.post("https://marketplace-api.wildberries.ru/api/v3/supplies").mock(
        return_value=respx.MockResponse(201, json={"id": "WB-GI-1234567"})
    )
    result = client.marketplace.create_supply(name="Test Supply")
    assert result["id"] == "WB-GI-1234567"


@respx.mock
def test_get_passes_offices(client: WBClient) -> None:
    """Тест get_passes_offices."""
    respx.get("https://marketplace-api.wildberries.ru/api/v3/passes/offices").mock(
        return_value=respx.MockResponse(200, json=[{"id": 1, "name": "Office", "address": "Addr"}])
    )
    result = client.marketplace.get_passes_offices()
    assert isinstance(result, list)
    assert result[0]["name"] == "Office"
