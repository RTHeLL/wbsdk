"""Тесты WBDAPI."""

import pytest
import respx

from wbsdk import WBClient

BASE_URL = "https://devapi-digital.wildberries.ru"


@pytest.fixture
def client() -> WBClient:
    return WBClient(token="test-token")


@respx.mock
def test_get_keys(client: WBClient) -> None:
    """Тест get_keys."""
    respx.get(f"{BASE_URL}/api/v1/keys-api/keys").mock(
        return_value=respx.MockResponse(200, json=[])
    )
    result = client.wbd.get_keys()
    assert result is not None


@respx.mock
def test_get_offers(client: WBClient) -> None:
    """Тест get_offers."""
    respx.get(f"{BASE_URL}/api/v1/offers").mock(return_value=respx.MockResponse(200, json=[]))
    result = client.wbd.get_offers()
    assert result is not None


@respx.mock
def test_get_offer(client: WBClient) -> None:
    """Тест get_offer."""
    respx.get(f"{BASE_URL}/api/v1/offers/123").mock(
        return_value=respx.MockResponse(200, json={"offer_id": 123})
    )
    result = client.wbd.get_offer(offer_id=123)
    assert result is not None


@respx.mock
def test_get_catalog(client: WBClient) -> None:
    """Тест get_catalog."""
    respx.get(f"{BASE_URL}/api/v1/catalog").mock(return_value=respx.MockResponse(200, json=[]))
    result = client.wbd.get_catalog()
    assert result is not None


@respx.mock
def test_content_upload_init(client: WBClient) -> None:
    """Тест content_upload_init."""
    respx.post(f"{BASE_URL}/api/v1/content/upload/init").mock(
        return_value=respx.MockResponse(200, json={"uploadId": "u-123"})
    )
    result = client.wbd.content_upload_init(payload={"offerId": 1, "fileName": "f"})
    assert result is not None
