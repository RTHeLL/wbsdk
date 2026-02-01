"""Тесты AnalyticsAPI."""

import pytest
import respx

from wbsdk import WBClient
from wbsdk.schemas.analytics import (
    NmReportCreateResponse,
    NmReportRetryResponse,
    NmReportsListResponse,
    SalesFunnelGroupedResponse,
    SalesFunnelHistoryResponse,
    SalesFunnelProductsResponse,
    SearchReportResponse,
    StocksGroupsResponse,
    StocksProductsResponse,
)

BASE_URL = "https://seller-analytics-api.wildberries.ru"


@pytest.fixture
def client() -> WBClient:
    return WBClient(token="test-token")


@respx.mock
def test_get_sales_funnel_products(client: WBClient) -> None:
    """Тест get_sales_funnel_products."""
    respx.post(f"{BASE_URL}/api/analytics/v3/sales-funnel/products").mock(
        return_value=respx.MockResponse(200, json={"data": [], "total": 0})
    )
    result = client.analytics.get_sales_funnel_products(
        selected_period={"begin": "2024-01-01", "end": "2024-01-31"}
    )
    assert isinstance(result, SalesFunnelProductsResponse)
    assert result.total == 0


@respx.mock
def test_get_sales_funnel_products_history(client: WBClient) -> None:
    """Тест get_sales_funnel_products_history."""
    respx.post(f"{BASE_URL}/api/analytics/v3/sales-funnel/products/history").mock(
        return_value=respx.MockResponse(200, json={"data": []})
    )
    result = client.analytics.get_sales_funnel_products_history(
        selected_period={"begin": "2024-01-01", "end": "2024-01-07"},
        nm_ids=[12345, 67890],
    )
    assert isinstance(result, SalesFunnelHistoryResponse)


@respx.mock
def test_get_sales_funnel_grouped_history(client: WBClient) -> None:
    """Тест get_sales_funnel_grouped_history."""
    respx.post(f"{BASE_URL}/api/analytics/v3/sales-funnel/grouped/history").mock(
        return_value=respx.MockResponse(200, json={"data": []})
    )
    result = client.analytics.get_sales_funnel_grouped_history(
        selected_period={"begin": "2024-01-01", "end": "2024-01-31"},
    )
    assert isinstance(result, SalesFunnelGroupedResponse)


@respx.mock
def test_get_search_report(client: WBClient) -> None:
    """Тест get_search_report."""
    respx.post(f"{BASE_URL}/api/v2/search-report/report").mock(
        return_value=respx.MockResponse(200, json={"data": [], "total": 0})
    )
    result = client.analytics.get_search_report(
        current_period={"begin": "2024-01-01", "end": "2024-01-31"},
        order_by={"field": "query", "mode": "asc"},
        limit=50,
        offset=0,
    )
    assert isinstance(result, SearchReportResponse)


@respx.mock
def test_get_stocks_groups(client: WBClient) -> None:
    """Тест get_stocks_groups."""
    respx.post(f"{BASE_URL}/api/v2/stocks-report/products/groups").mock(
        return_value=respx.MockResponse(200, json={"data": [], "total": 0})
    )
    result = client.analytics.get_stocks_groups(
        current_period={"begin": "2024-01-01", "end": "2024-01-31"},
        stock_type="wb",
        skip_deleted_nm=True,
        availability_filters=[],
        order_by={"field": "nmID", "mode": "asc"},
        offset=0,
    )
    assert isinstance(result, StocksGroupsResponse)


@respx.mock
def test_get_stocks_products(client: WBClient) -> None:
    """Тест get_stocks_products."""
    respx.post(f"{BASE_URL}/api/v2/stocks-report/products/products").mock(
        return_value=respx.MockResponse(200, json={"data": [], "total": 0})
    )
    result = client.analytics.get_stocks_products(
        current_period={"begin": "2024-01-01", "end": "2024-01-31"},
        stock_type="wb",
        skip_deleted_nm=True,
        order_by={"field": "nmID", "mode": "asc"},
        availability_filters=[],
        offset=0,
    )
    assert isinstance(result, StocksProductsResponse)


@respx.mock
def test_create_nm_report(client: WBClient) -> None:
    """Тест create_nm_report."""
    respx.post(f"{BASE_URL}/api/v2/nm-report/downloads").mock(
        return_value=respx.MockResponse(200, json={"downloadID": "rep-123"})
    )
    result = client.analytics.create_nm_report(
        report_id="rep-123",
        report_type="sales",
        params={"param1": "value1"},
    )
    assert isinstance(result, NmReportCreateResponse)
    assert result.download_id == "rep-123"


@respx.mock
def test_get_nm_reports_list(client: WBClient) -> None:
    """Тест get_nm_reports_list."""
    respx.get(f"{BASE_URL}/api/v2/nm-report/downloads").mock(
        return_value=respx.MockResponse(
            200,
            json={
                "data": [
                    {
                        "downloadID": "rep-123",
                        "reportType": "sales",
                        "status": "done",
                        "createdAt": "2024-01-01T00:00:00",
                        "updatedAt": "2024-01-01T01:00:00",
                    }
                ]
            },
        )
    )
    result = client.analytics.get_nm_reports_list()
    assert isinstance(result, NmReportsListResponse)
    assert len(result.data) == 1


@respx.mock
def test_retry_nm_report(client: WBClient) -> None:
    """Тест retry_nm_report."""
    respx.post(f"{BASE_URL}/api/v2/nm-report/downloads/retry").mock(
        return_value=respx.MockResponse(200, json={"data": {}, "error": False})
    )
    result = client.analytics.retry_nm_report(download_id="rep-123")
    assert isinstance(result, NmReportRetryResponse)
    assert result.error is False


@respx.mock
def test_get_nm_report_file(client: WBClient) -> None:
    """Тест get_nm_report_file."""
    respx.get(f"{BASE_URL}/api/v2/nm-report/downloads/file/rep-123").mock(
        return_value=respx.MockResponse(200, content=b"csv,data,here")
    )
    result = client.analytics.get_nm_report_file(download_id="rep-123")
    assert isinstance(result, bytes)
    assert result == b"csv,data,here"
