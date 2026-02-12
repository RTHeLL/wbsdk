"""Тесты PromotionAPI и PromotionCalendarAPI."""

import pytest
import respx

from wbsdk import WBClient

ADVERT_BASE_URL = "https://advert-api.wildberries.ru"
DP_CALENDAR_BASE_URL = "https://dp-calendar-api.wildberries.ru"


@pytest.fixture
def client() -> WBClient:
    return WBClient(token="test-token")


@respx.mock
def test_get_promotion_count(client: WBClient) -> None:
    """Тест get_promotion_count."""
    respx.get(f"{ADVERT_BASE_URL}/adv/v1/promotion/count").mock(
        return_value=respx.MockResponse(200, json={"adverts": [], "all": 0})
    )
    result = client.promotion.get_promotion_count()
    assert result is not None
    assert "adverts" in result or "all" in result


@respx.mock
def test_get_adverts(client: WBClient) -> None:
    """Тест get_adverts."""
    respx.get(f"{ADVERT_BASE_URL}/api/advert/v2/adverts").mock(
        return_value=respx.MockResponse(200, json=[])
    )
    result = client.promotion.get_adverts()
    assert result is not None


@respx.mock
def test_get_balance(client: WBClient) -> None:
    """Тест get_balance (рекламный счёт)."""
    respx.get(f"{ADVERT_BASE_URL}/adv/v1/balance").mock(
        return_value=respx.MockResponse(200, json={"balance": 1000})
    )
    result = client.promotion.get_balance()
    assert result is not None


@respx.mock
def test_get_auction_placements(client: WBClient) -> None:
    """Тест get_auction_placements."""
    respx.get(f"{ADVERT_BASE_URL}/adv/v0/auction/placements").mock(
        return_value=respx.MockResponse(200, json=[])
    )
    result = client.promotion.get_auction_placements()
    assert result is not None


@respx.mock
def test_promotion_calendar_get_promotions(client: WBClient) -> None:
    """Тест promotion_calendar.get_promotions."""
    respx.get(f"{DP_CALENDAR_BASE_URL}/api/v1/calendar/promotions").mock(
        return_value=respx.MockResponse(200, json=[])
    )
    result = client.promotion_calendar.get_promotions(params={})
    assert result is not None
