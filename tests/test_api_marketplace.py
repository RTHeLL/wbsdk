"""Тесты MarketplaceAPI."""

import pytest
import respx

from wbsdk import WBClient
from wbsdk.schemas import (
    BarcodeResponse,
    CrossBorderStickersResponse,
    OrderMetaResponse,
    OrdersClientInfoResponse,
    OrdersResponse,
    OrdersStatusResponse,
    Pass,
    PassCreateResponse,
    PassOffice,
    ReshipmentResponse,
    StickersResponse,
    Supply,
    SupplyBoxesResponse,
    SupplyOrderIdsResponse,
    SuppliesResponse,
    TrbxIdsResponse,
    TrbxStickersResponse,
)

BASE_URL = "https://marketplace-api.wildberries.ru"


@pytest.fixture
def client() -> WBClient:
    return WBClient(token="test-token")


@respx.mock
def test_get_new_orders(client: WBClient) -> None:
    """Тест get_new_orders."""
    respx.get(f"{BASE_URL}/api/v3/orders/new").mock(
        return_value=respx.MockResponse(200, json={"orders": []})
    )
    result = client.marketplace.get_new_orders()
    assert result.orders == []


@respx.mock
def test_get_orders(client: WBClient) -> None:
    """Тест get_orders."""
    respx.get(f"{BASE_URL}/api/v3/orders").mock(
        return_value=respx.MockResponse(200, json={"orders": [], "next": 0})
    )
    result = client.marketplace.get_orders(limit=10, next_cursor=0)
    assert isinstance(result, OrdersResponse)
    assert result.orders == []


@respx.mock
def test_get_orders_status(client: WBClient) -> None:
    """Тест get_orders_status."""
    respx.post(f"{BASE_URL}/api/v3/orders/status").mock(
        return_value=respx.MockResponse(
            200,
            json={"orders": [{"id": 1, "supplierStatus": "confirm", "wbStatus": "confirm"}]},
        )
    )
    result = client.marketplace.get_orders_status(order_ids=[1])
    assert isinstance(result, OrdersStatusResponse)
    assert len(result.orders) == 1


@respx.mock
def test_get_orders_reshipment(client: WBClient) -> None:
    """Тест get_orders_reshipment."""
    respx.get(f"{BASE_URL}/api/v3/supplies/orders/reshipment").mock(
        return_value=respx.MockResponse(200, json={"orders": []})
    )
    result = client.marketplace.get_orders_reshipment()
    assert isinstance(result, ReshipmentResponse)
    assert result.orders == []


@respx.mock
def test_cancel_order(client: WBClient) -> None:
    """Тест cancel_order."""
    respx.patch(f"{BASE_URL}/api/v3/orders/1/cancel").mock(
        return_value=respx.MockResponse(200)
    )
    client.marketplace.cancel_order(order_id=1)


@respx.mock
def test_get_orders_stickers(client: WBClient) -> None:
    """Тест get_orders_stickers."""
    respx.post(f"{BASE_URL}/api/v3/orders/stickers").mock(
        return_value=respx.MockResponse(200, json={"stickers": []})
    )
    result = client.marketplace.get_orders_stickers(order_ids=[1])
    assert isinstance(result, StickersResponse)
    assert result.stickers == []


@respx.mock
def test_get_cross_border_stickers(client: WBClient) -> None:
    """Тест get_cross_border_stickers."""
    respx.post(f"{BASE_URL}/api/v3/orders/stickers/cross-border").mock(
        return_value=respx.MockResponse(200, json={"stickers": []})
    )
    result = client.marketplace.get_cross_border_stickers(order_ids=[1])
    assert isinstance(result, CrossBorderStickersResponse)


@respx.mock
def test_get_orders_client_info(client: WBClient) -> None:
    """Тест get_orders_client_info."""
    respx.post(f"{BASE_URL}/api/v3/orders/client").mock(
        return_value=respx.MockResponse(200, json={"orders": []})
    )
    result = client.marketplace.get_orders_client_info(order_ids=[1])
    assert isinstance(result, OrdersClientInfoResponse)


@respx.mock
def test_get_orders_metadata(client: WBClient) -> None:
    """Тест get_orders_metadata."""
    respx.post(f"{BASE_URL}/api/marketplace/v3/orders/meta").mock(
        return_value=respx.MockResponse(200, json={"meta": {}})
    )
    result = client.marketplace.get_orders_metadata(order_ids=[1])
    assert isinstance(result, OrderMetaResponse)


@respx.mock
def test_delete_order_metadata(client: WBClient) -> None:
    """Тест delete_order_metadata."""
    respx.delete(f"{BASE_URL}/api/v3/orders/1/meta").mock(
        return_value=respx.MockResponse(204)
    )
    client.marketplace.delete_order_metadata(order_id=1)


@respx.mock
def test_add_order_sgtin(client: WBClient) -> None:
    """Тест add_order_sgtin."""
    respx.put(f"{BASE_URL}/api/v3/orders/1/meta/sgtin").mock(
        return_value=respx.MockResponse(200)
    )
    client.marketplace.add_order_sgtin(order_id=1, sgtins=["01046007880001702115"])


@respx.mock
def test_add_order_uin(client: WBClient) -> None:
    """Тест add_order_uin."""
    respx.put(f"{BASE_URL}/api/v3/orders/1/meta/uin").mock(
        return_value=respx.MockResponse(200)
    )
    client.marketplace.add_order_uin(order_id=1, uin="12345678901234")


@respx.mock
def test_add_order_imei(client: WBClient) -> None:
    """Тест add_order_imei."""
    respx.put(f"{BASE_URL}/api/v3/orders/1/meta/imei").mock(
        return_value=respx.MockResponse(200)
    )
    client.marketplace.add_order_imei(order_id=1, imei="123456789012345")


@respx.mock
def test_add_order_gtin(client: WBClient) -> None:
    """Тест add_order_gtin."""
    respx.put(f"{BASE_URL}/api/v3/orders/1/meta/gtin").mock(
        return_value=respx.MockResponse(200)
    )
    client.marketplace.add_order_gtin(order_id=1, gtin="4601234567890")


@respx.mock
def test_add_order_expiration(client: WBClient) -> None:
    """Тест add_order_expiration."""
    respx.put(f"{BASE_URL}/api/v3/orders/1/meta/expiration").mock(
        return_value=respx.MockResponse(200)
    )
    client.marketplace.add_order_expiration(order_id=1, expiration="01.01.2025")


@respx.mock
def test_add_order_customs_declaration(client: WBClient) -> None:
    """Тест add_order_customs_declaration."""
    respx.put(f"{BASE_URL}/api/marketplace/v3/orders/1/meta/customs-declaration").mock(
        return_value=respx.MockResponse(200)
    )
    client.marketplace.add_order_customs_declaration(
        order_id=1, customs_declaration="10702010/010124/1234567"
    )


@respx.mock
def test_create_supply(client: WBClient) -> None:
    """Тест create_supply."""
    respx.post(f"{BASE_URL}/api/v3/supplies").mock(
        return_value=respx.MockResponse(201, json={"id": "WB-GI-1234567"})
    )
    result = client.marketplace.create_supply(name="Test Supply")
    assert result.id == "WB-GI-1234567"


@respx.mock
def test_get_supplies(client: WBClient) -> None:
    """Тест get_supplies."""
    respx.get(f"{BASE_URL}/api/v3/supplies").mock(
        return_value=respx.MockResponse(200, json={"supplies": [], "next": 0})
    )
    result = client.marketplace.get_supplies(limit=10, next_cursor=0)
    assert isinstance(result, SuppliesResponse)
    assert result.supplies == []


@respx.mock
def test_add_orders_to_supply(client: WBClient) -> None:
    """Тест add_orders_to_supply."""
    respx.patch(f"{BASE_URL}/api/marketplace/v3/supplies/WB-GI-123/orders").mock(
        return_value=respx.MockResponse(200)
    )
    client.marketplace.add_orders_to_supply(supply_id="WB-GI-123", order_ids=[1, 2])


@respx.mock
def test_get_supply_details(client: WBClient) -> None:
    """Тест get_supply_details."""
    respx.get(f"{BASE_URL}/api/v3/supplies/WB-GI-123").mock(
        return_value=respx.MockResponse(
            200,
            json={"id": "WB-GI-123", "done": False, "createdAt": "2024-01-01"},
        )
    )
    result = client.marketplace.get_supply_details(supply_id="WB-GI-123")
    assert isinstance(result, Supply)
    assert result.id == "WB-GI-123"


@respx.mock
def test_delete_supply(client: WBClient) -> None:
    """Тест delete_supply."""
    respx.delete(f"{BASE_URL}/api/v3/supplies/WB-GI-123").mock(
        return_value=respx.MockResponse(204)
    )
    client.marketplace.delete_supply(supply_id="WB-GI-123")


@respx.mock
def test_get_supply_order_ids(client: WBClient) -> None:
    """Тест get_supply_order_ids."""
    respx.get(f"{BASE_URL}/api/marketplace/v3/supplies/WB-GI-123/order-ids").mock(
        return_value=respx.MockResponse(200, json={"orders": [1, 2]})
    )
    result = client.marketplace.get_supply_order_ids(supply_id="WB-GI-123")
    assert isinstance(result, SupplyOrderIdsResponse)
    assert result.orders == [1, 2]


@respx.mock
def test_deliver_supply(client: WBClient) -> None:
    """Тест deliver_supply."""
    respx.patch(f"{BASE_URL}/api/v3/supplies/WB-GI-123/deliver").mock(
        return_value=respx.MockResponse(200)
    )
    client.marketplace.deliver_supply(supply_id="WB-GI-123")


@respx.mock
def test_get_supply_barcode(client: WBClient) -> None:
    """Тест get_supply_barcode."""
    respx.get(f"{BASE_URL}/api/v3/supplies/WB-GI-123/barcode").mock(
        return_value=respx.MockResponse(200, json={"barcode": "data", "file": "base64..."})
    )
    result = client.marketplace.get_supply_barcode(supply_id="WB-GI-123")
    assert isinstance(result, BarcodeResponse)
    assert result.barcode == "data"


@respx.mock
def test_get_supply_boxes(client: WBClient) -> None:
    """Тест get_supply_boxes."""
    respx.get(f"{BASE_URL}/api/v3/supplies/WB-GI-123/trbx").mock(
        return_value=respx.MockResponse(200, json={"trbxes": [{"id": "trbx-1", "orders": []}]})
    )
    result = client.marketplace.get_supply_boxes(supply_id="WB-GI-123")
    assert isinstance(result, SupplyBoxesResponse)
    assert len(result.trbxes) == 1


@respx.mock
def test_add_boxes_to_supply(client: WBClient) -> None:
    """Тест add_boxes_to_supply."""
    respx.post(f"{BASE_URL}/api/v3/supplies/WB-GI-123/trbx").mock(
        return_value=respx.MockResponse(200, json={"trbxIds": ["trbx-1", "trbx-2"]})
    )
    result = client.marketplace.add_boxes_to_supply(supply_id="WB-GI-123", amount=2)
    assert isinstance(result, TrbxIdsResponse)
    assert result.trbx_ids == ["trbx-1", "trbx-2"]


@respx.mock
def test_delete_boxes_from_supply(client: WBClient) -> None:
    """Тест delete_boxes_from_supply."""
    respx.delete(f"{BASE_URL}/api/v3/supplies/WB-GI-123/trbx").mock(
        return_value=respx.MockResponse(200)
    )
    client.marketplace.delete_boxes_from_supply(
        supply_id="WB-GI-123", trbx_ids=["trbx-1", "trbx-2"]
    )


@respx.mock
def test_get_supply_box_stickers(client: WBClient) -> None:
    """Тест get_supply_box_stickers."""
    respx.post(f"{BASE_URL}/api/v3/supplies/WB-GI-123/trbx/stickers").mock(
        return_value=respx.MockResponse(200, json={"stickers": [{"id": "1", "file": "base64"}]})
    )
    result = client.marketplace.get_supply_box_stickers(
        supply_id="WB-GI-123", trbx_ids=["trbx-1"]
    )
    assert isinstance(result, TrbxStickersResponse)
    assert len(result.stickers) == 1


@respx.mock
def test_get_passes_offices(client: WBClient) -> None:
    """Тест get_passes_offices."""
    respx.get(f"{BASE_URL}/api/v3/passes/offices").mock(
        return_value=respx.MockResponse(200, json=[{"id": 1, "name": "Office", "address": "Addr"}])
    )
    result = client.marketplace.get_passes_offices()
    assert isinstance(result, list)
    assert all(isinstance(x, PassOffice) for x in result)
    assert result[0].name == "Office"


@respx.mock
def test_get_passes(client: WBClient) -> None:
    """Тест get_passes."""
    respx.get(f"{BASE_URL}/api/v3/passes").mock(
        return_value=respx.MockResponse(
            200,
            json=[{"id": 1, "firstName": "Иван", "lastName": "Иванов", "carModel": "Lada", "carNumber": "A123BC", "officeId": 1}],
        )
    )
    result = client.marketplace.get_passes()
    assert isinstance(result, list)
    assert all(isinstance(x, Pass) for x in result)
    assert result[0].first_name == "Иван"


@respx.mock
def test_create_pass(client: WBClient) -> None:
    """Тест create_pass."""
    respx.post(f"{BASE_URL}/api/v3/passes").mock(
        return_value=respx.MockResponse(201, json={"id": 42})
    )
    result = client.marketplace.create_pass(
        first_name="Иван",
        last_name="Иванов",
        car_model="Lada",
        car_number="A123BC",
        office_id=1,
    )
    assert isinstance(result, PassCreateResponse)
    assert result.id == 42


@respx.mock
def test_update_pass(client: WBClient) -> None:
    """Тест update_pass."""
    respx.put(f"{BASE_URL}/api/v3/passes/1").mock(
        return_value=respx.MockResponse(200)
    )
    client.marketplace.update_pass(
        pass_id=1,
        first_name="Иван",
        last_name="Иванов",
        car_model="Lada",
        car_number="A123BC",
        office_id=1,
    )


@respx.mock
def test_delete_pass(client: WBClient) -> None:
    """Тест delete_pass."""
    respx.delete(f"{BASE_URL}/api/v3/passes/1").mock(
        return_value=respx.MockResponse(204)
    )
    client.marketplace.delete_pass(pass_id=1)
