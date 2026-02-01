"""Тесты ContentAPI."""

import pytest
import respx

from wbsdk import WBClient
from wbsdk.schemas import SubjectsResponse, TagsResponse


@pytest.fixture
def client() -> WBClient:
    return WBClient(token="test-token")


@respx.mock
def test_get_subjects(client: WBClient) -> None:
    """Тест get_subjects."""
    respx.get("https://content-api.wildberries.ru/content/v2/object/all").mock(
        return_value=respx.MockResponse(
            200,
            json={
                "data": [
                    {"subjectID": 105, "subjectName": "Кроссовки", "parentID": 1, "parentName": "Обувь"}
                ],
                "error": False,
            },
        )
    )
    result = client.content.get_subjects(limit=10, offset=0)
    assert isinstance(result, SubjectsResponse)
    assert len(result.data) == 1
    assert result.data[0].subject_name == "Кроссовки"


@respx.mock
def test_get_tags(client: WBClient) -> None:
    """Тест get_tags."""
    respx.get("https://content-api.wildberries.ru/content/v2/tags").mock(
        return_value=respx.MockResponse(
            200,
            json={"data": [{"id": 1, "name": "Sale", "color": "D1CFD7"}], "error": False},
        )
    )
    result = client.content.get_tags()
    assert isinstance(result, TagsResponse)
    assert len(result.data) == 1
    assert result.data[0].name == "Sale"


@respx.mock
def test_create_tag(client: WBClient) -> None:
    """Тест create_tag."""
    respx.post("https://content-api.wildberries.ru/content/v2/tag").mock(
        return_value=respx.MockResponse(200, json={"data": None, "error": False})
    )
    result = client.content.create_tag(name="NewTag", color="D1CFD7")
    assert result is not None
    assert result.error is False
