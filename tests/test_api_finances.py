"""Тесты FinancesAPI и DocumentsAPI."""

import pytest
import respx

from wbsdk import WBClient

FINANCE_BASE_URL = "https://finance-api.wildberries.ru"
DOCUMENTS_BASE_URL = "https://documents-api.wildberries.ru"


@pytest.fixture
def client() -> WBClient:
    return WBClient(token="test-token")


@respx.mock
def test_finances_get_balance(client: WBClient) -> None:
    """Тест finances.get_balance."""
    respx.get(f"{FINANCE_BASE_URL}/api/v1/account/balance").mock(
        return_value=respx.MockResponse(
            200,
            json={
                "currency": "RUB",
                "current": 10196.21,
                "for_withdraw": 6395.8,
            },
        )
    )
    result = client.finances.get_balance()
    assert result is not None
    assert result.get("currency") == "RUB"


@respx.mock
def test_documents_get_categories(client: WBClient) -> None:
    """Тест documents.get_categories."""
    respx.get(f"{DOCUMENTS_BASE_URL}/api/v1/documents/categories").mock(
        return_value=respx.MockResponse(200, json=[])
    )
    result = client.documents.get_categories()
    assert result is not None


@respx.mock
def test_documents_get_documents_list(client: WBClient) -> None:
    """Тест documents.get_documents_list."""
    respx.get(f"{DOCUMENTS_BASE_URL}/api/v1/documents/list").mock(
        return_value=respx.MockResponse(200, json={"data": []})
    )
    result = client.documents.get_documents_list(params={"limit": 10})
    assert result is not None
