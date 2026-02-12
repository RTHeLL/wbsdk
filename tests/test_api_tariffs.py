"""Тесты TariffsAPI."""

import pytest
import respx

from wbsdk import WBClient
from wbsdk.schemas.tariffs import TariffsResponse

BASE_URL = "https://common-api.wildberries.ru"


@pytest.fixture
def client() -> WBClient:
    return WBClient(token="test-token")


@respx.mock
def test_get_commission(client: WBClient) -> None:
    """Тест get_commission."""
    respx.get(f"{BASE_URL}/api/v1/tariffs/commission").mock(
        return_value=respx.MockResponse(200, json={"report": []})
    )
    result = client.tariffs.get_commission()
    assert isinstance(result, TariffsResponse)
    assert result.report == []


@respx.mock
def test_get_tariffs_box(client: WBClient) -> None:
    """Тест get_tariffs_box."""
    respx.get(f"{BASE_URL}/api/v1/tariffs/box").mock(
        return_value=respx.MockResponse(200, json={"data": {}})
    )
    result = client.tariffs.get_tariffs_box(date="2024-01-01")
    assert isinstance(result, TariffsResponse)


@respx.mock
def test_get_tariffs_pallet(client: WBClient) -> None:
    """Тест get_tariffs_pallet."""
    respx.get(f"{BASE_URL}/api/v1/tariffs/pallet").mock(
        return_value=respx.MockResponse(200, json={"data": {}})
    )
    result = client.tariffs.get_tariffs_pallet(date="2024-01-01")
    assert isinstance(result, TariffsResponse)


@respx.mock
def test_get_tariffs_return(client: WBClient) -> None:
    """Тест get_tariffs_return."""
    respx.get(f"{BASE_URL}/api/v1/tariffs/return").mock(
        return_value=respx.MockResponse(200, json={"data": {}})
    )
    result = client.tariffs.get_tariffs_return(date="2024-01-01")
    assert isinstance(result, TariffsResponse)


@respx.mock
def test_get_acceptance_coefficients(client: WBClient) -> None:
    """Тест get_acceptance_coefficients."""
    respx.get(f"{BASE_URL}/api/tariffs/v1/acceptance/coefficients").mock(
        return_value=respx.MockResponse(200, json=[{"warehouseID": 1, "coefficient": 0}])
    )
    result = client.tariffs.get_acceptance_coefficients()
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["warehouseID"] == 1
