"""Тесты CommunicationsAPI."""

import pytest
import respx

from wbsdk import WBClient

BASE_URL = "https://feedbacks-api.wildberries.ru"


@pytest.fixture
def client() -> WBClient:
    return WBClient(token="test-token")


@respx.mock
def test_get_new_feedbacks_questions(client: WBClient) -> None:
    """Тест get_new_feedbacks_questions."""
    respx.get(f"{BASE_URL}/api/v1/new-feedbacks-questions").mock(
        return_value=respx.MockResponse(
            200,
            json={"data": {"hasNewQuestions": False, "hasNewFeedbacks": False}, "error": False},
        )
    )
    result = client.communications.get_new_feedbacks_questions()
    assert result is not None
    assert result.get("error") is False


@respx.mock
def test_get_questions_count_unanswered(client: WBClient) -> None:
    """Тест get_questions_count_unanswered."""
    respx.get(f"{BASE_URL}/api/v1/questions/count-unanswered").mock(
        return_value=respx.MockResponse(
            200,
            json={"data": {"countUnanswered": 0, "countUnansweredToday": 0}, "error": False},
        )
    )
    result = client.communications.get_questions_count_unanswered()
    assert result is not None


@respx.mock
def test_get_feedbacks(client: WBClient) -> None:
    """Тест get_feedbacks."""
    respx.post(f"{BASE_URL}/api/v1/feedbacks").mock(
        return_value=respx.MockResponse(200, json={"feedbacks": [], "count": 0})
    )
    result = client.communications.get_feedbacks(payload={"skip": 0, "take": 10})
    assert result is not None


@respx.mock
def test_get_pins_count(client: WBClient) -> None:
    """Тест get_pins_count."""
    respx.get(f"{BASE_URL}/api/feedbacks/v1/pins/count").mock(
        return_value=respx.MockResponse(200, json={"count": 0})
    )
    result = client.communications.get_pins_count()
    assert result is not None


@respx.mock
def test_get_claims(client: WBClient) -> None:
    """Тест get_claims."""
    respx.post(f"{BASE_URL}/api/v1/claims").mock(
        return_value=respx.MockResponse(200, json={"claims": []})
    )
    result = client.communications.get_claims(payload={"skip": 0, "take": 10})
    assert result is not None
