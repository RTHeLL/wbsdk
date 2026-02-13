"""Тесты асинхронного клиента."""

import asyncio
import time

import pytest
import respx

from wbsdk import AsyncWBClient
from wbsdk.exceptions import WBAuthError


def test_async_client_requires_token() -> None:
    """Клиент требует непустой токен."""
    with pytest.raises(ValueError):
        AsyncWBClient(token="")


async def test_async_client_creates_with_token(token: str) -> None:
    """Клиент создаётся с валидным токеном."""
    client = AsyncWBClient(token=token)
    assert client._token == token
    await client.close()


async def test_async_client_context_manager(token: str) -> None:
    """Клиент поддерживает async context manager."""
    async with AsyncWBClient(token=token) as client:
        assert client._token == token
    # После выхода соединение закрыто
    assert client._http_client.is_closed


async def test_async_client_content_api(token: str) -> None:
    """Доступ к ContentAPI через свойство (тот же класс, что у WBClient)."""
    async with AsyncWBClient(token=token) as client:
        content = client.content
        assert content is not None
        assert content._base_url == "https://content-api.wildberries.ru"


async def test_async_client_prices_api(token: str) -> None:
    """Доступ к PricesAPI через свойство."""
    async with AsyncWBClient(token=token) as client:
        prices = client.prices
        assert prices is not None


async def test_async_client_marketplace_api(token: str) -> None:
    """Доступ к MarketplaceAPI через свойство."""
    async with AsyncWBClient(token=token) as client:
        marketplace = client.marketplace
        assert marketplace is not None


async def test_async_client_warehouses_api(token: str) -> None:
    """Доступ к WarehousesAPI через свойство."""
    async with AsyncWBClient(token=token) as client:
        warehouses = client.warehouses
        assert warehouses is not None


async def test_async_client_analytics_api(token: str) -> None:
    """Доступ к AnalyticsAPI через свойство."""
    async with AsyncWBClient(token=token) as client:
        analytics = client.analytics
        assert analytics is not None


async def test_async_client_general_api(token: str) -> None:
    """Доступ к GeneralAPI через свойство."""
    async with AsyncWBClient(token=token) as client:
        assert client.general is not None
        assert client.general._base_url == "https://common-api.wildberries.ru"


async def test_async_client_user_management_api(token: str) -> None:
    """Доступ к UserManagementAPI через свойство."""
    async with AsyncWBClient(token=token) as client:
        assert client.user_management is not None


async def test_async_client_tariffs_api(token: str) -> None:
    """Доступ к TariffsAPI через свойство."""
    async with AsyncWBClient(token=token) as client:
        assert client.tariffs is not None


async def test_async_client_orders_dbw_api(token: str) -> None:
    """Доступ к OrdersDBWAPI через свойство."""
    async with AsyncWBClient(token=token) as client:
        assert client.orders_dbw is not None


async def test_async_client_orders_dbs_api(token: str) -> None:
    """Доступ к OrdersDBSAPI через свойство."""
    async with AsyncWBClient(token=token) as client:
        assert client.orders_dbs is not None


async def test_async_client_click_collect_api(token: str) -> None:
    """Доступ к ClickCollectAPI через свойство."""
    async with AsyncWBClient(token=token) as client:
        assert client.click_collect is not None


async def test_async_client_orders_fbw_api(token: str) -> None:
    """Доступ к OrdersFBWAPI через свойство."""
    async with AsyncWBClient(token=token) as client:
        assert client.orders_fbw is not None
        assert client.orders_fbw._base_url == "https://supplies-api.wildberries.ru"


async def test_async_client_communications_api(token: str) -> None:
    """Доступ к CommunicationsAPI через свойство."""
    async with AsyncWBClient(token=token) as client:
        assert client.communications is not None


async def test_async_client_reports_api(token: str) -> None:
    """Доступ к ReportsAPI через свойство."""
    async with AsyncWBClient(token=token) as client:
        assert client.reports is not None


async def test_async_client_promotion_api(token: str) -> None:
    """Доступ к PromotionAPI и PromotionCalendarAPI через свойства."""
    async with AsyncWBClient(token=token) as client:
        assert client.promotion is not None
        assert client.promotion_calendar is not None


async def test_async_client_finances_documents_api(token: str) -> None:
    """Доступ к FinancesAPI и DocumentsAPI через свойства."""
    async with AsyncWBClient(token=token) as client:
        assert client.finances is not None
        assert client.documents is not None


async def test_async_client_wbd_api(token: str) -> None:
    """Доступ к WBDAPI через свойство."""
    async with AsyncWBClient(token=token) as client:
        assert client.wbd is not None


@respx.mock
async def test_async_general_ping(token: str) -> None:
    """GeneralAPI.ping возвращает данные при await."""
    respx.get("https://common-api.wildberries.ru/ping").mock(
        return_value=respx.MockResponse(
            200,
            json={"TS": "2024-01-01T12:00:00+03:00", "Status": "OK"},
        )
    )
    async with AsyncWBClient(token=token) as client:
        result = await client.general.ping()
    assert result.status == "OK"


async def test_async_client_content_api_sandbox(token: str) -> None:
    """При sandbox=True ContentAPI использует sandbox URL."""
    async with AsyncWBClient(token=token, sandbox=True) as client:
        content = client.content
        assert content._base_url == "https://content-api-sandbox.wildberries.ru"


@respx.mock
async def test_async_sandbox_request_goes_to_sandbox_url(token: str) -> None:
    """При sandbox=True запрос уходит на content-api-sandbox."""
    route = respx.get(
        "https://content-api-sandbox.wildberries.ru/content/v2/object/parent/all"
    ).mock(return_value=respx.MockResponse(200, json={"data": [], "error": False}))
    async with AsyncWBClient(token=token, sandbox=True) as client:
        await client.content.get_parent_categories()
    assert route.called


@respx.mock
async def test_async_request_adds_authorization(token: str) -> None:
    """Запрос добавляет заголовок Authorization."""
    route = respx.get("https://content-api.wildberries.ru/content/v2/object/parent/all").mock(
        return_value=respx.MockResponse(200, json={"data": [], "error": False})
    )
    async with AsyncWBClient(token=token) as client:
        await client.content.get_parent_categories()
    assert route.called
    assert route.calls.last.request.headers.get("Authorization") == token


@respx.mock
async def test_async_request_raises_on_401(token: str) -> None:
    """Запрос выбрасывает WBAuthError при 401."""
    respx.get("https://content-api.wildberries.ru/content/v2/object/parent/all").mock(
        return_value=respx.MockResponse(401, json={"errorText": "Unauthorized"})
    )
    async with AsyncWBClient(token=token) as client:
        with pytest.raises(WBAuthError):
            await client.content.get_parent_categories()


@respx.mock
async def test_async_content_get_parent_categories(token: str) -> None:
    """ContentAPI.get_parent_categories возвращает данные при await."""
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
    async with AsyncWBClient(token=token) as client:
        result = await client.content.get_parent_categories()
    assert result.data is not None
    assert len(result.data) == 1
    assert result.data[0].name == "Категория"


@respx.mock
async def test_async_event_loop_not_blocked(token: str) -> None:
    """Проверка асинхронности

    Пока один "медленный" запрос ждёт ответа, другая корутина должна выполняться.
    Если бы request блокировал поток (time.sleep и т.п.), счётчик бы не рос.
    """
    delay_sec = 0.1
    ticks: list[float] = []

    async def slow_response(request):
        await asyncio.sleep(delay_sec)
        return respx.MockResponse(
            200,
            json={"data": [], "error": False},
        )

    async def ticker():
        deadline = time.perf_counter() + delay_sec + 0.05
        while time.perf_counter() < deadline:
            ticks.append(time.perf_counter())
            await asyncio.sleep(0.02)

    respx.get("https://content-api.wildberries.ru/content/v2/object/parent/all").mock(
        side_effect=slow_response
    )

    async with AsyncWBClient(token=token) as client:
        tick_task = asyncio.create_task(ticker())
        await client.content.get_parent_categories()
        await tick_task

    # За время ожидания HTTP (delay_sec) ticker должен был сделать несколько тиков.
    assert len(ticks) >= 2, f"Event loop был заблокирован во время запроса (ticks={len(ticks)})"
