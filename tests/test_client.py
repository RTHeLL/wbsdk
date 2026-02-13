"""Тесты базового клиента."""

import logging

import pytest
import respx

from wbsdk import WBClient
from wbsdk.exceptions import WBAuthError, WBValidationError


def test_client_requires_token() -> None:
    """Клиент требует непустой токен."""
    with pytest.raises(ValueError):
        WBClient(token="")


def test_client_creates_with_token(token: str) -> None:
    """Клиент создаётся с валидным токеном."""
    client = WBClient(token=token)
    assert client._token == token
    client.close()


def test_client_context_manager(token: str) -> None:
    """Клиент поддерживает context manager."""
    with WBClient(token=token) as client:
        assert client._token == token
    # После выхода соединение закрыто
    assert client._http_client.is_closed


def test_client_content_api(token: str) -> None:
    """Доступ к ContentAPI через свойство."""
    with WBClient(token=token) as client:
        content = client.content
        assert content is not None
        assert content._base_url == "https://content-api.wildberries.ru"


def test_client_prices_api(token: str) -> None:
    """Доступ к PricesAPI через свойство."""
    with WBClient(token=token) as client:
        prices = client.prices
        assert prices is not None


def test_client_marketplace_api(token: str) -> None:
    """Доступ к MarketplaceAPI через свойство."""
    with WBClient(token=token) as client:
        marketplace = client.marketplace
        assert marketplace is not None


def test_client_warehouses_api(token: str) -> None:
    """Доступ к WarehousesAPI через свойство."""
    with WBClient(token=token) as client:
        warehouses = client.warehouses
        assert warehouses is not None


def test_client_analytics_api(token: str) -> None:
    """Доступ к AnalyticsAPI через свойство."""
    with WBClient(token=token) as client:
        analytics = client.analytics
        assert analytics is not None


def test_client_general_api(token: str) -> None:
    """Доступ к GeneralAPI через свойство."""
    with WBClient(token=token) as client:
        assert client.general is not None
        assert client.general._base_url == "https://common-api.wildberries.ru"


def test_client_user_management_tariffs_api(token: str) -> None:
    """Доступ к UserManagementAPI и TariffsAPI через свойства."""
    with WBClient(token=token) as client:
        assert client.user_management is not None
        assert client.tariffs is not None


def test_client_orders_apis(token: str) -> None:
    """Доступ к OrdersDBWAPI, OrdersDBSAPI, ClickCollectAPI, OrdersFBWAPI."""
    with WBClient(token=token) as client:
        assert client.orders_dbw is not None
        assert client.orders_dbs is not None
        assert client.click_collect is not None
        assert client.orders_fbw is not None


def test_client_communications_reports_api(token: str) -> None:
    """Доступ к CommunicationsAPI и ReportsAPI через свойства."""
    with WBClient(token=token) as client:
        assert client.communications is not None
        assert client.reports is not None


def test_client_promotion_finances_documents_wbd_api(token: str) -> None:
    """Доступ к PromotionAPI, FinancesAPI, DocumentsAPI, WBDAPI через свойства."""
    with WBClient(token=token) as client:
        assert client.promotion is not None
        assert client.promotion_calendar is not None
        assert client.finances is not None
        assert client.documents is not None
        assert client.wbd is not None


def test_client_content_api_sandbox(token: str) -> None:
    """При sandbox=True ContentAPI использует sandbox URL."""
    with WBClient(token=token, sandbox=True) as client:
        content = client.content
        assert content._base_url == "https://content-api-sandbox.wildberries.ru"


@respx.mock
def test_sandbox_request_goes_to_sandbox_url(token: str) -> None:
    """При sandbox=True запрос уходит на content-api-sandbox."""
    route = respx.get(
        "https://content-api-sandbox.wildberries.ru/content/v2/object/parent/all"
    ).mock(
        return_value=respx.MockResponse(200, json={"data": [], "error": False})
    )
    with WBClient(token=token, sandbox=True) as client:
        client.content.get_parent_categories()
    assert route.called


def test_base_urls_override_sandbox(token: str) -> None:
    """При явном base_urls параметр sandbox не меняет URL (приоритет у base_urls)."""
    custom_url = "https://custom-content.example"
    with WBClient(
        token=token,
        sandbox=True,
        base_urls={"content": custom_url},
    ) as client:
        content = client.content
        assert content._base_url == custom_url


@respx.mock
def test_request_adds_authorization(token: str) -> None:
    """Запрос добавляет заголовок Authorization."""
    route = respx.get("https://content-api.wildberries.ru/content/v2/object/parent/all").mock(
        return_value=respx.MockResponse(200, json={"data": [], "error": False})
    )
    with WBClient(token=token) as client:
        client.content.get_parent_categories()
    assert route.called
    assert route.calls.last.request.headers.get("Authorization") == token


@respx.mock
def test_request_raises_on_401(token: str) -> None:
    """Запрос выбрасывает WBAuthError при 401."""
    respx.get("https://content-api.wildberries.ru/content/v2/object/parent/all").mock(
        return_value=respx.MockResponse(401, json={"errorText": "Unauthorized"})
    )
    with WBClient(token=token) as client:
        with pytest.raises(WBAuthError):
            client.content.get_parent_categories()


@respx.mock
def test_request_raises_on_400(token: str) -> None:
    """Запрос выбрасывает WBValidationError при 400."""
    respx.post("https://discounts-prices-api.wildberries.ru/api/v2/upload/task").mock(
        return_value=respx.MockResponse(400, json={"errorText": "Bad request"})
    )
    with WBClient(token=token) as client:
        with pytest.raises(WBValidationError):
            client.prices.set_prices([{"nmID": 1, "price": -1, "discount": 0}])


@respx.mock
def test_content_get_parent_categories(token: str) -> None:
    """ContentAPI.get_parent_categories возвращает данные."""
    respx.get("https://content-api.wildberries.ru/content/v2/object/parent/all").mock(
        return_value=respx.MockResponse(
            200,
            json={
                "data": [{"id": 1, "name": "Категория", "isVisible": True}],
                "error": False,
                "errorText": "",
            },
        )
    )
    with WBClient(token=token) as client:
        result = client.content.get_parent_categories()
    assert result.data is not None
    assert len(result.data) == 1
    assert result.data[0].name == "Категория"


@respx.mock
def test_debug_logs_request_and_response(caplog: pytest.LogCaptureFixture, token: str) -> None:
    """При debug=True в лог выводятся запрос и ответ, токен не логируется."""
    caplog.set_level(logging.DEBUG, logger="wbsdk")
    respx.get("https://content-api.wildberries.ru/content/v2/object/parent/all").mock(
        return_value=respx.MockResponse(200, json={"data": [], "error": False})
    )
    with WBClient(token=token, debug=True) as client:
        client.content.get_parent_categories()
    log_text = caplog.text
    assert "WB API request:" in log_text
    assert "GET" in log_text
    assert "content-api.wildberries.ru" in log_text or "content/v2/object" in log_text
    assert "domain=content" in log_text
    assert "WB API response:" in log_text
    assert "200" in log_text
    assert token not in log_text


@respx.mock
def test_debug_false_no_debug_logs_with_info_level(caplog: pytest.LogCaptureFixture, token: str) -> None:
    """При debug=False и уровне INFO отладочные сообщения wbsdk не выводятся."""
    caplog.set_level(logging.INFO, logger="wbsdk")
    respx.get("https://content-api.wildberries.ru/content/v2/object/parent/all").mock(
        return_value=respx.MockResponse(200, json={"data": [], "error": False})
    )
    with WBClient(token=token, debug=False) as client:
        client.content.get_parent_categories()
    wbsdk_logs = [r for r in caplog.records if r.name == "wbsdk"]
    assert not wbsdk_logs
