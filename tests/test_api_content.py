"""Тесты ContentAPI."""

import tempfile
from pathlib import Path

import pytest
import respx

from wbsdk import WBClient
from wbsdk.schemas import (
    BarcodesResponse,
    BrandsResponse,
    CardsLimitsResponse,
    CardsListResponse,
    ContentMutationResponse,
    DirectoryItem,
    DirectoryListResponse,
    ParentCategoriesResponse,
    SubjectCharacteristicsResponse,
    SubjectsResponse,
    TagMutationResponse,
    TagsResponse,
    TnvedResponse,
)

BASE_URL = "https://content-api.wildberries.ru"


@pytest.fixture
def client() -> WBClient:
    return WBClient(token="test-token")


@respx.mock
def test_get_parent_categories(client: WBClient) -> None:
    """Тест get_parent_categories."""
    respx.get(f"{BASE_URL}/content/v2/object/parent/all").mock(
        return_value=respx.MockResponse(
            200,
            json={"data": [{"id": 1, "name": "Обувь"}], "error": False},
        )
    )
    result = client.content.get_parent_categories()
    assert isinstance(result, ParentCategoriesResponse)
    assert len(result.data) == 1
    assert result.data[0].name == "Обувь"


@respx.mock
def test_get_subjects(client: WBClient) -> None:
    """Тест get_subjects."""
    respx.get(f"{BASE_URL}/content/v2/object/all").mock(
        return_value=respx.MockResponse(
            200,
            json={
                "data": [
                    {
                        "subjectID": 105,
                        "subjectName": "Кроссовки",
                        "parentID": 1,
                        "parentName": "Обувь",
                    }
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
def test_get_subject_characteristics(client: WBClient) -> None:
    """Тест get_subject_characteristics."""
    respx.get(f"{BASE_URL}/content/v2/object/charcs/105").mock(
        return_value=respx.MockResponse(
            200,
            json={"data": [{"id": 1, "name": "Цвет", "required": True}], "error": False},
        )
    )
    result = client.content.get_subject_characteristics(subject_id=105)
    assert isinstance(result, SubjectCharacteristicsResponse)
    assert len(result.data) == 1
    first = result.data[0]
    name = first.name if hasattr(first, "name") else first["name"]
    assert name == "Цвет"


@respx.mock
def test_get_colors(client: WBClient) -> None:
    """Тест get_colors."""
    respx.get(f"{BASE_URL}/content/v2/directory/colors").mock(
        return_value=respx.MockResponse(200, json=[{"id": 1, "name": "Чёрный"}])
    )
    result = client.content.get_colors()
    assert isinstance(result, DirectoryListResponse)
    assert isinstance(result.data, list)
    assert all(isinstance(x, DirectoryItem) for x in result.data)
    assert result.data[0].name == "Чёрный"


@respx.mock
def test_get_genders(client: WBClient) -> None:
    """Тест get_genders."""
    respx.get(f"{BASE_URL}/content/v2/directory/kinds").mock(
        return_value=respx.MockResponse(200, json=[{"id": 1, "name": "Мужской"}])
    )
    result = client.content.get_genders()
    assert isinstance(result, DirectoryListResponse)
    assert isinstance(result.data, list)
    assert all(isinstance(x, DirectoryItem) for x in result.data)


@respx.mock
def test_get_countries(client: WBClient) -> None:
    """Тест get_countries."""
    respx.get(f"{BASE_URL}/content/v2/directory/countries").mock(
        return_value=respx.MockResponse(200, json=[{"id": 1, "name": "Россия"}])
    )
    result = client.content.get_countries()
    assert isinstance(result, DirectoryListResponse)
    assert isinstance(result.data, list)
    assert all(isinstance(x, DirectoryItem) for x in result.data)


@respx.mock
def test_get_seasons(client: WBClient) -> None:
    """Тест get_seasons."""
    respx.get(f"{BASE_URL}/content/v2/directory/seasons").mock(
        return_value=respx.MockResponse(200, json=[{"id": 1, "name": "Всесезонный"}])
    )
    result = client.content.get_seasons()
    assert isinstance(result, DirectoryListResponse)
    assert isinstance(result.data, list)
    assert all(isinstance(x, DirectoryItem) for x in result.data)


@respx.mock
def test_get_vat_rates(client: WBClient) -> None:
    """Тест get_vat_rates."""
    respx.get(f"{BASE_URL}/content/v2/directory/vat").mock(
        return_value=respx.MockResponse(200, json=[{"id": 1, "name": "20%"}])
    )
    result = client.content.get_vat_rates()
    assert isinstance(result, DirectoryListResponse)
    assert isinstance(result.data, list)
    assert all(isinstance(x, DirectoryItem) for x in result.data)


@respx.mock
def test_get_tnved(client: WBClient) -> None:
    """Тест get_tnved."""
    respx.get(f"{BASE_URL}/content/v2/directory/tnved").mock(
        return_value=respx.MockResponse(200, json={"data": [], "error": False})
    )
    result = client.content.get_tnved(subject_id=105)
    assert isinstance(result, TnvedResponse)
    assert result.error is False


@respx.mock
def test_get_brands(client: WBClient) -> None:
    """Тест get_brands."""
    respx.get(f"{BASE_URL}/api/content/v1/brands").mock(
        return_value=respx.MockResponse(
            200,
            json={"data": [{"id": 1, "name": "Brand"}], "next": None, "error": False},
        )
    )
    result = client.content.get_brands(subject_id=105)
    assert isinstance(result, BrandsResponse)
    assert len(result.data) == 1


@respx.mock
def test_get_cards_limits(client: WBClient) -> None:
    """Тест get_cards_limits."""
    respx.get(f"{BASE_URL}/content/v2/cards/limits").mock(
        return_value=respx.MockResponse(200, json={"data": {"cardsTotal": 100}, "error": False})
    )
    result = client.content.get_cards_limits()
    assert isinstance(result, CardsLimitsResponse)
    assert result.data is not None


@respx.mock
def test_generate_barcodes(client: WBClient) -> None:
    """Тест generate_barcodes."""
    respx.post(f"{BASE_URL}/content/v2/barcodes").mock(
        return_value=respx.MockResponse(
            200,
            json={"data": ["4601234567890", "4601234567891"], "error": False},
        )
    )
    result = client.content.generate_barcodes(count=2)
    assert isinstance(result, BarcodesResponse)
    assert len(result.data) == 2


@respx.mock
def test_create_cards(client: WBClient) -> None:
    """Тест create_cards."""
    respx.post(f"{BASE_URL}/content/v2/cards/upload").mock(
        return_value=respx.MockResponse(200, json={"data": None, "error": False})
    )
    result = client.content.create_cards(cards=[{"vendorCode": "test"}])
    assert isinstance(result, ContentMutationResponse)
    assert result.error is False


@respx.mock
def test_create_cards_with_merge(client: WBClient) -> None:
    """Тест create_cards_with_merge."""
    respx.post(f"{BASE_URL}/content/v2/cards/upload/add").mock(
        return_value=respx.MockResponse(200, json={"data": None, "error": False})
    )
    result = client.content.create_cards_with_merge(imt_id=100, cards_to_add=[{}])
    assert isinstance(result, ContentMutationResponse)
    assert result.error is False


@respx.mock
def test_get_cards_list(client: WBClient) -> None:
    """Тест get_cards_list."""
    respx.post(f"{BASE_URL}/content/v2/get/cards/list").mock(
        return_value=respx.MockResponse(200, json={"data": [], "cursor": None, "error": False})
    )
    result = client.content.get_cards_list(settings={"cursor": {}})
    assert isinstance(result, CardsListResponse)
    assert result.error is False


@respx.mock
def test_get_cards_error_list(client: WBClient) -> None:
    """Тест get_cards_error_list."""
    respx.post(f"{BASE_URL}/content/v2/cards/error/list").mock(
        return_value=respx.MockResponse(200, json={"data": [], "cursor": None, "error": False})
    )
    result = client.content.get_cards_error_list(cursor={})
    assert isinstance(result, CardsListResponse)


@respx.mock
def test_update_cards(client: WBClient) -> None:
    """Тест update_cards."""
    respx.post(f"{BASE_URL}/content/v2/cards/update").mock(
        return_value=respx.MockResponse(200, json={"data": None, "error": False})
    )
    result = client.content.update_cards(cards=[{"nmID": 123}])
    assert isinstance(result, ContentMutationResponse)


@respx.mock
def test_move_cards(client: WBClient) -> None:
    """Тест move_cards."""
    respx.post(f"{BASE_URL}/content/v2/cards/moveNm").mock(
        return_value=respx.MockResponse(200, json={"data": None, "error": False})
    )
    result = client.content.move_cards(target_imt=100, nm_ids=[123, 456])
    assert isinstance(result, ContentMutationResponse)


@respx.mock
def test_move_cards_to_trash(client: WBClient) -> None:
    """Тест move_cards_to_trash."""
    respx.post(f"{BASE_URL}/content/v2/cards/delete/trash").mock(
        return_value=respx.MockResponse(200, json={"data": None, "error": False})
    )
    result = client.content.move_cards_to_trash(nm_ids=[123])
    assert isinstance(result, ContentMutationResponse)


@respx.mock
def test_recover_cards_from_trash(client: WBClient) -> None:
    """Тест recover_cards_from_trash."""
    respx.post(f"{BASE_URL}/content/v2/cards/recover").mock(
        return_value=respx.MockResponse(200, json={"data": None, "error": False})
    )
    result = client.content.recover_cards_from_trash(nm_ids=[123])
    assert isinstance(result, ContentMutationResponse)


@respx.mock
def test_get_cards_trash_list(client: WBClient) -> None:
    """Тест get_cards_trash_list."""
    respx.post(f"{BASE_URL}/content/v2/get/cards/trash").mock(
        return_value=respx.MockResponse(200, json={"data": [], "cursor": None, "error": False})
    )
    result = client.content.get_cards_trash_list(settings={})
    assert isinstance(result, CardsListResponse)


@respx.mock
def test_upload_media_file(client: WBClient) -> None:
    """Тест upload_media_file."""
    respx.post(f"{BASE_URL}/content/v3/media/file").mock(
        return_value=respx.MockResponse(200, json={"data": None, "error": False})
    )
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
        f.write(b"fake image content")
        f.flush()
        result = client.content.upload_media_file(
            nm_id=123, photo_number=1, file_path=f.name
        )
    Path(f.name).unlink(missing_ok=True)
    assert isinstance(result, ContentMutationResponse)
    assert result.error is False


@respx.mock
def test_upload_media_by_links(client: WBClient) -> None:
    """Тест upload_media_by_links."""
    respx.post(f"{BASE_URL}/content/v3/media/save").mock(
        return_value=respx.MockResponse(200, json={"data": None, "error": False})
    )
    result = client.content.upload_media_by_links(
        nm_id=123, data=["https://example.com/image.jpg"]
    )
    assert isinstance(result, ContentMutationResponse)


@respx.mock
def test_get_tags(client: WBClient) -> None:
    """Тест get_tags."""
    respx.get(f"{BASE_URL}/content/v2/tags").mock(
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
    respx.post(f"{BASE_URL}/content/v2/tag").mock(
        return_value=respx.MockResponse(200, json={"data": None, "error": False})
    )
    result = client.content.create_tag(name="NewTag", color="D1CFD7")
    assert result is not None
    assert result.error is False


@respx.mock
def test_update_tag(client: WBClient) -> None:
    """Тест update_tag."""
    respx.patch(f"{BASE_URL}/content/v2/tag/1").mock(
        return_value=respx.MockResponse(200, json={"data": None, "error": False})
    )
    result = client.content.update_tag(tag_id=1, name="UpdatedTag", color="FF0000")
    assert isinstance(result, TagMutationResponse)
    assert result.error is False


@respx.mock
def test_delete_tag(client: WBClient) -> None:
    """Тест delete_tag."""
    respx.delete(f"{BASE_URL}/content/v2/tag/1").mock(
        return_value=respx.MockResponse(204)
    )
    client.content.delete_tag(tag_id=1)


@respx.mock
def test_link_tags_to_card(client: WBClient) -> None:
    """Тест link_tags_to_card."""
    respx.post(f"{BASE_URL}/content/v2/tag/nomenclature/link").mock(
        return_value=respx.MockResponse(200, json={"data": None, "error": False})
    )
    result = client.content.link_tags_to_card(nm_id=123, tags_ids=[1, 2])
    assert isinstance(result, ContentMutationResponse)
