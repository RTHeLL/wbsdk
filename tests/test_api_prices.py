"""Тесты PricesAPI."""

import pytest
import respx

from wbsdk import WBClient
from wbsdk.schemas.prices import (
    GoodsSizesResponse,
    GoodsWithPricesResponse,
    PriceUploadResponse,
    QuarantineGoodsResponse,
    UploadDetailsResponse,
    UploadStateResponse,
)

BASE_URL = "https://discounts-prices-api.wildberries.ru"


@pytest.fixture
def client() -> WBClient:
    return WBClient(token="test-token")


@respx.mock
def test_set_prices(client: WBClient) -> None:
    """Тест set_prices."""
    respx.post(f"{BASE_URL}/api/v2/upload/task").mock(
        return_value=respx.MockResponse(200, json={"uploadID": 12345})
    )
    result = client.prices.set_prices(data=[{"nmId": 123, "price": 1000}])
    assert isinstance(result, PriceUploadResponse)
    assert result.upload_id == 12345


@respx.mock
def test_set_size_prices(client: WBClient) -> None:
    """Тест set_size_prices."""
    respx.post(f"{BASE_URL}/api/v2/upload/task/size").mock(
        return_value=respx.MockResponse(200, json={"uploadID": 12346})
    )
    result = client.prices.set_size_prices(data=[{"nmId": 123, "chrtId": 456, "price": 1000}])
    assert isinstance(result, PriceUploadResponse)
    assert result.upload_id == 12346


@respx.mock
def test_set_club_discounts(client: WBClient) -> None:
    """Тест set_club_discounts."""
    respx.post(f"{BASE_URL}/api/v2/upload/task/club-discount").mock(
        return_value=respx.MockResponse(200, json={"uploadID": 12347})
    )
    result = client.prices.set_club_discounts(data=[{"nmId": 123, "discount": 10}])
    assert isinstance(result, PriceUploadResponse)
    assert result.upload_id == 12347


@respx.mock
def test_get_processed_upload_state(client: WBClient) -> None:
    """Тест get_processed_upload_state."""
    respx.get(f"{BASE_URL}/api/v2/history/tasks").mock(
        return_value=respx.MockResponse(200, json={"uploadID": 12345, "data": []})
    )
    result = client.prices.get_processed_upload_state(upload_id=12345)
    assert isinstance(result, UploadStateResponse)
    assert result.upload_id == 12345


@respx.mock
def test_get_processed_upload_details(client: WBClient) -> None:
    """Тест get_processed_upload_details."""
    respx.get(f"{BASE_URL}/api/v2/history/goods/task").mock(
        return_value=respx.MockResponse(200, json={"data": [], "total": 0})
    )
    result = client.prices.get_processed_upload_details(upload_id=12345)
    assert isinstance(result, UploadDetailsResponse)
    assert result.total == 0


@respx.mock
def test_get_unprocessed_upload_state(client: WBClient) -> None:
    """Тест get_unprocessed_upload_state."""
    respx.get(f"{BASE_URL}/api/v2/buffer/tasks").mock(
        return_value=respx.MockResponse(200, json={"uploadID": 12345, "data": []})
    )
    result = client.prices.get_unprocessed_upload_state(upload_id=12345)
    assert isinstance(result, UploadStateResponse)
    assert result.upload_id == 12345


@respx.mock
def test_get_unprocessed_upload_details(client: WBClient) -> None:
    """Тест get_unprocessed_upload_details."""
    respx.get(f"{BASE_URL}/api/v2/buffer/goods/task").mock(
        return_value=respx.MockResponse(200, json={"data": [], "total": 0})
    )
    result = client.prices.get_unprocessed_upload_details(upload_id=12345)
    assert isinstance(result, UploadDetailsResponse)
    assert result.total == 0


@respx.mock
def test_get_goods_with_prices(client: WBClient) -> None:
    """Тест get_goods_with_prices."""
    respx.get(f"{BASE_URL}/api/v2/list/goods/filter").mock(
        return_value=respx.MockResponse(
            200,
            json={
                "data": [{"nmID": 123, "price": 1000, "discount": 10}],
                "total": 1,
            },
        )
    )
    result = client.prices.get_goods_with_prices(limit=100, offset=0)
    assert isinstance(result, GoodsWithPricesResponse)
    assert len(result.data) == 1
    assert result.data[0].nm_id == 123


@respx.mock
def test_get_goods_with_prices_by_articles(client: WBClient) -> None:
    """Тест get_goods_with_prices_by_articles."""
    respx.post(f"{BASE_URL}/api/v2/list/goods/filter").mock(
        return_value=respx.MockResponse(
            200,
            json={
                "data": [{"nmID": 123, "price": 1000}],
                "total": 1,
            },
        )
    )
    result = client.prices.get_goods_with_prices_by_articles(nm_list=[123, 456])
    assert isinstance(result, GoodsWithPricesResponse)
    assert len(result.data) == 1


@respx.mock
def test_get_goods_sizes_with_prices(client: WBClient) -> None:
    """Тест get_goods_sizes_with_prices."""
    respx.get(f"{BASE_URL}/api/v2/list/goods/size/nm").mock(
        return_value=respx.MockResponse(
            200,
            json={
                "data": [{"chrtID": 456, "nmID": 123, "price": 1000}],
                "total": 1,
            },
        )
    )
    result = client.prices.get_goods_sizes_with_prices(nm_id=123)
    assert isinstance(result, GoodsSizesResponse)
    assert len(result.data) == 1
    assert result.data[0].chrt_id == 456


@respx.mock
def test_get_quarantine_goods(client: WBClient) -> None:
    """Тест get_quarantine_goods."""
    respx.get(f"{BASE_URL}/api/v2/quarantine/goods").mock(
        return_value=respx.MockResponse(
            200,
            json={
                "data": [{"nmID": 123, "error": "Invalid price"}],
                "total": 1,
            },
        )
    )
    result = client.prices.get_quarantine_goods()
    assert isinstance(result, QuarantineGoodsResponse)
    assert len(result.data) == 1
    assert result.data[0].nm_id == 123
