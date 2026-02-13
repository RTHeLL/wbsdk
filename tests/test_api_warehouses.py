"""Тесты WarehousesAPI."""

import pytest
import respx

from wbsdk import WBClient
from wbsdk.schemas.warehouses import (
    Office,
    StocksResponse,
    StoreContact,
    Warehouse,
    WarehouseCreateResponse,
)

BASE_URL = "https://marketplace-api.wildberries.ru"


@pytest.fixture
def client() -> WBClient:
    return WBClient(token="test-token")


@respx.mock
def test_get_offices(client: WBClient) -> None:
    """Тест get_offices."""
    respx.get(f"{BASE_URL}/api/v3/offices").mock(
        return_value=respx.MockResponse(
            200,
            json=[{"id": 1, "name": "Офис 1", "address": "ул. Тестовая, 1"}],
        )
    )
    result = client.warehouses.get_offices()
    assert isinstance(result, list)
    assert all(isinstance(x, Office) for x in result)
    assert result[0].id == 1
    assert result[0].name == "Офис 1"


@respx.mock
def test_get_warehouses(client: WBClient) -> None:
    """Тест get_warehouses."""
    respx.get(f"{BASE_URL}/api/v3/warehouses").mock(
        return_value=respx.MockResponse(
            200,
            json=[{"id": 1, "name": "Склад 1", "officeId": 10}],
        )
    )
    result = client.warehouses.get_warehouses()
    assert isinstance(result, list)
    assert all(isinstance(x, Warehouse) for x in result)
    assert result[0].id == 1
    assert result[0].name == "Склад 1"


@respx.mock
def test_create_warehouse(client: WBClient) -> None:
    """Тест create_warehouse."""
    respx.post(f"{BASE_URL}/api/v3/warehouses").mock(
        return_value=respx.MockResponse(201, json={"id": 42})
    )
    result = client.warehouses.create_warehouse(name="Новый склад", office_id=1)
    assert isinstance(result, WarehouseCreateResponse)
    assert result.id == 42


@respx.mock
def test_update_warehouse(client: WBClient) -> None:
    """Тест update_warehouse."""
    respx.put(f"{BASE_URL}/api/v3/warehouses/1").mock(
        return_value=respx.MockResponse(200, json=None)
    )
    client.warehouses.update_warehouse(warehouse_id=1, name="Обновлённый склад", office_id=1)


@respx.mock
def test_delete_warehouse(client: WBClient) -> None:
    """Тест delete_warehouse."""
    respx.delete(f"{BASE_URL}/api/v3/warehouses/1").mock(return_value=respx.MockResponse(204))
    client.warehouses.delete_warehouse(warehouse_id=1)


@respx.mock
def test_get_warehouse_contacts(client: WBClient) -> None:
    """Тест get_warehouse_contacts."""
    respx.get(f"{BASE_URL}/api/v3/dbw/warehouses/1/contacts").mock(
        return_value=respx.MockResponse(
            200,
            json=[{"contactType": "phone", "contact": "+79001234567"}],
        )
    )
    result = client.warehouses.get_warehouse_contacts(warehouse_id=1)
    assert isinstance(result, list)
    assert all(isinstance(x, StoreContact) for x in result)
    assert result[0].contact_type == "phone"


@respx.mock
def test_update_warehouse_contacts(client: WBClient) -> None:
    """Тест update_warehouse_contacts."""
    respx.put(f"{BASE_URL}/api/v3/dbw/warehouses/1/contacts").mock(
        return_value=respx.MockResponse(200)
    )
    client.warehouses.update_warehouse_contacts(
        warehouse_id=1,
        contacts=[{"contactType": "phone", "contact": "+79001234567"}],
    )


@respx.mock
def test_update_stocks(client: WBClient) -> None:
    """Тест update_stocks."""
    respx.put(f"{BASE_URL}/api/v3/stocks/1").mock(return_value=respx.MockResponse(200))
    client.warehouses.update_stocks(
        warehouse_id=1,
        stocks=[{"chrtId": 123, "sku": "ABC", "amount": 10}],
    )


@respx.mock
def test_delete_stocks(client: WBClient) -> None:
    """Тест delete_stocks."""
    respx.delete(f"{BASE_URL}/api/v3/stocks/1").mock(return_value=respx.MockResponse(200))
    client.warehouses.delete_stocks(warehouse_id=1, chrt_ids=[123, 456])


@respx.mock
def test_get_stocks(client: WBClient) -> None:
    """Тест get_stocks."""
    respx.post(f"{BASE_URL}/api/v3/stocks/1").mock(
        return_value=respx.MockResponse(
            200,
            json={"stocks": [{"sku": "ABC", "amount": 10, "chrtId": 123}]},
        )
    )
    result = client.warehouses.get_stocks(warehouse_id=1)
    assert isinstance(result, StocksResponse)
    assert len(result.stocks) == 1
    assert result.stocks[0].sku == "ABC"
    assert result.stocks[0].amount == 10
