"""Тесты ReportsAPI."""

import pytest
import respx

from wbsdk import WBClient

BASE_URL = "https://statistics-api.wildberries.ru"


@pytest.fixture
def client() -> WBClient:
    return WBClient(token="test-token")


@respx.mock
def test_get_incomes(client: WBClient) -> None:
    """Тест get_incomes."""
    respx.get(f"{BASE_URL}/api/v1/supplier/incomes").mock(
        return_value=respx.MockResponse(200, json=[])
    )
    result = client.reports.get_incomes(
        date_from="2024-01-01", date_to="2024-01-31"
    )
    assert result == []


@respx.mock
def test_get_stocks(client: WBClient) -> None:
    """Тест get_stocks."""
    respx.get(f"{BASE_URL}/api/v1/supplier/stocks").mock(
        return_value=respx.MockResponse(200, json=[])
    )
    result = client.reports.get_stocks(
        date_from="2024-01-01", date_to="2024-01-31"
    )
    assert result == []


@respx.mock
def test_get_orders(client: WBClient) -> None:
    """Тест get_orders."""
    respx.get(f"{BASE_URL}/api/v1/supplier/orders").mock(
        return_value=respx.MockResponse(200, json=[])
    )
    result = client.reports.get_orders(
        date_from="2024-01-01", date_to="2024-01-31"
    )
    assert result == []


@respx.mock
def test_get_sales(client: WBClient) -> None:
    """Тест get_sales."""
    respx.get(f"{BASE_URL}/api/v1/supplier/sales").mock(
        return_value=respx.MockResponse(200, json=[])
    )
    result = client.reports.get_sales(
        date_from="2024-01-01", date_to="2024-01-31"
    )
    assert result == []


@respx.mock
def test_get_report_detail_by_period(client: WBClient) -> None:
    """Тест get_report_detail_by_period."""
    respx.get(f"{BASE_URL}/api/v5/supplier/reportDetailByPeriod").mock(
        return_value=respx.MockResponse(200, json=[])
    )
    result = client.reports.get_report_detail_by_period(
        date_from="2024-01-01", date_to="2024-01-31"
    )
    assert result == []
