"""Тесты GeneralAPI."""

import pytest
import respx

from wbsdk import WBClient
from wbsdk.schemas.general import NewsResponse, PingResponse, SellerInfoResponse

BASE_URL = "https://common-api.wildberries.ru"


@pytest.fixture
def client() -> WBClient:
    return WBClient(token="test-token")


@respx.mock
def test_ping(client: WBClient) -> None:
    """Тест ping."""
    respx.get(f"{BASE_URL}/ping").mock(
        return_value=respx.MockResponse(200, json={"TS": "2024-01-01T12:00:00+03:00", "Status": "OK"})
    )
    result = client.general.ping()
    assert isinstance(result, PingResponse)
    assert result.status == "OK"


@respx.mock
def test_get_news(client: WBClient) -> None:
    """Тест get_news."""
    respx.get(f"{BASE_URL}/api/communications/v2/news").mock(
        return_value=respx.MockResponse(200, json={"data": []})
    )
    result = client.general.get_news(from_date="2024-01-01")
    assert isinstance(result, NewsResponse)
    assert result.data == []


@respx.mock
def test_get_seller_info(client: WBClient) -> None:
    """Тест get_seller_info."""
    respx.get(f"{BASE_URL}/api/v1/seller-info").mock(
        return_value=respx.MockResponse(
            200,
            json={"name": "ИП Тест", "sid": "uuid-123", "tradeMark": "Test Store"},
        )
    )
    result = client.general.get_seller_info()
    assert isinstance(result, SellerInfoResponse)
    assert result.name == "ИП Тест"
    assert result.sid == "uuid-123"
    assert result.trade_mark == "Test Store"
