"""Тесты базового клиента."""

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
    assert "data" in result
    assert len(result["data"]) == 1
    assert result["data"][0]["name"] == "Категория"
