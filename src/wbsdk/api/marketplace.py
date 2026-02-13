"""API заказов FBS, поставок и пропусков."""

from typing import Any

from wbsdk.api.base import BaseAPI
from wbsdk.schemas.marketplace import (
    BarcodeResponse,
    CrossBorderStickersResponse,
    OrderMetaResponse,
    OrdersClientInfoResponse,
    OrdersNewResponse,
    OrdersResponse,
    OrdersStatusHistoryResponse,
    OrdersStatusResponse,
    Pass,
    PassCreateResponse,
    PassOffice,
    ReshipmentResponse,
    StickersResponse,
    SuppliesResponse,
    Supply,
    SupplyBoxesResponse,
    SupplyCreateResponse,
    SupplyOrderIdsResponse,
    TrbxIdsResponse,
    TrbxStickersResponse,
)


class MarketplaceAPI(BaseAPI):
    """API для работы с заказами FBS, поставками и пропусками."""

    def __init__(self, client: Any, base_url: str):
        super().__init__(client, base_url, domain="marketplace")

    # --- Заказы ---

    def get_new_orders(self) -> OrdersNewResponse:
        """Новые сборочные задания."""
        return self.get("/api/v3/orders/new", response_model=OrdersNewResponse)

    def get_orders(
        self,
        limit: int,
        next_cursor: int,
        *,
        date_from: int | None = None,
        date_to: int | None = None,
    ) -> OrdersResponse:
        """Список сборочных заданий за период (макс. 30 дней)."""
        params: dict[str, Any] = {"limit": limit, "next": next_cursor}
        if date_from is not None:
            params["dateFrom"] = date_from
        if date_to is not None:
            params["dateTo"] = date_to
        return self.get("/api/v3/orders", params=params, response_model=OrdersResponse)

    def get_orders_status(self, order_ids: list[int]) -> OrdersStatusResponse:
        """Статусы сборочных заданий."""
        return self.post(
            "/api/v3/orders/status",
            json={"orders": order_ids},
            response_model=OrdersStatusResponse,
        )

    def get_orders_status_history(self, order_ids: list[int]) -> OrdersStatusHistoryResponse:
        """История статусов сборочных заданий кроссбордера (до 100 заказов)."""
        return self.post(
            "/api/v3/orders/status/history",
            json={"orders": order_ids},
            response_model=OrdersStatusHistoryResponse,
        )

    def get_orders_reshipment(self) -> ReshipmentResponse:
        """Заказы, требующие переотправки."""
        return self.get(
            "/api/v3/supplies/orders/reshipment",
            response_model=ReshipmentResponse,
        )

    def cancel_order(self, order_id: int) -> None:
        """Отмена сборочного задания."""
        self.patch(f"/api/v3/orders/{order_id}/cancel")

    def get_orders_stickers(
        self,
        order_ids: list[int],
        *,
        sticker_type: str = "svg",
        width: int = 58,
        height: int = 40,
    ) -> StickersResponse:
        """Стикеры для заказов (svg, zplv, zplh, png)."""
        return self.post(
            "/api/v3/orders/stickers",
            params={"type": sticker_type, "width": width, "height": height},
            json={"orders": order_ids},
            response_model=StickersResponse,
        )

    def get_cross_border_stickers(self, order_ids: list[int]) -> CrossBorderStickersResponse:
        """Стикеры для кросс-бордер заказов (PDF)."""
        return self.post(
            "/api/v3/orders/stickers/cross-border",
            json={"orders": order_ids},
            response_model=CrossBorderStickersResponse,
        )

    def get_orders_client_info(self, order_ids: list[int]) -> OrdersClientInfoResponse:
        """Информация о клиенте по заказам (кросс-бордер Турция)."""
        return self.post(
            "/api/v3/orders/client",
            json={"orders": order_ids},
            response_model=OrdersClientInfoResponse,
        )

    # --- Метаданные заказов ---

    def get_orders_metadata(self, order_ids: list[int]) -> OrderMetaResponse:
        """Метаданные заказов."""
        return self.post(
            "/api/marketplace/v3/orders/meta",
            json={"orders": order_ids},
            response_model=OrderMetaResponse,
        )

    def delete_order_metadata(self, order_id: int, *, key: str | None = None) -> None:
        """Удаление метаданных заказа."""
        params = {}
        if key:
            params["key"] = key
        self.delete(f"/api/v3/orders/{order_id}/meta", params=params or None)

    def add_order_sgtin(self, order_id: int, sgtins: list[str]) -> None:
        """Добавление Data Matrix к заказу."""
        self.put(f"/api/v3/orders/{order_id}/meta/sgtin", json={"sgtins": sgtins})

    def add_order_uin(self, order_id: int, uin: str) -> None:
        """Добавление УИН к заказу."""
        self.put(f"/api/v3/orders/{order_id}/meta/uin", json={"uin": uin})

    def add_order_imei(self, order_id: int, imei: str) -> None:
        """Добавление IMEI к заказу."""
        self.put(f"/api/v3/orders/{order_id}/meta/imei", json={"imei": imei})

    def add_order_gtin(self, order_id: int, gtin: str) -> None:
        """Добавление GTIN к заказу."""
        self.put(f"/api/v3/orders/{order_id}/meta/gtin", json={"gtin": gtin})

    def add_order_expiration(self, order_id: int, expiration: str) -> None:
        """Добавление срока годности к заказу (формат dd.mm.yyyy)."""
        self.put(f"/api/v3/orders/{order_id}/meta/expiration", json={"expiration": expiration})

    def add_order_customs_declaration(self, order_id: int, customs_declaration: str) -> None:
        """Добавление номера ГТД к заказу."""
        self.put(
            f"/api/marketplace/v3/orders/{order_id}/meta/customs-declaration",
            json={"customsDeclaration": customs_declaration},
        )

    # --- Поставки ---

    def create_supply(self, name: str) -> SupplyCreateResponse:
        """Создание поставки."""
        return self.post(
            "/api/v3/supplies",
            json={"name": name},
            response_model=SupplyCreateResponse,
        )

    def get_supplies(self, limit: int, next_cursor: int) -> SuppliesResponse:
        """Список поставок."""
        return self.get(
            "/api/v3/supplies",
            params={"limit": limit, "next": next_cursor},
            response_model=SuppliesResponse,
        )

    def add_orders_to_supply(self, supply_id: str, order_ids: list[int]) -> None:
        """Добавление заказов в поставку."""
        self.patch(
            f"/api/marketplace/v3/supplies/{supply_id}/orders",
            json={"orders": order_ids},
        )

    def get_supply_details(self, supply_id: str) -> Supply:
        """Детали поставки."""
        return self.get(
            f"/api/v3/supplies/{supply_id}",
            response_model=Supply,
        )

    def delete_supply(self, supply_id: str) -> None:
        """Удаление поставки (если пуста)."""
        self.delete(f"/api/v3/supplies/{supply_id}")

    def get_supply_order_ids(self, supply_id: str) -> SupplyOrderIdsResponse:
        """ID заказов в поставке."""
        return self.get(
            f"/api/marketplace/v3/supplies/{supply_id}/order-ids",
            response_model=SupplyOrderIdsResponse,
        )

    def deliver_supply(self, supply_id: str) -> None:
        """Перевод поставки в доставку."""
        self.patch(f"/api/v3/supplies/{supply_id}/deliver")

    def get_supply_barcode(self, supply_id: str, *, barcode_type: str = "svg") -> BarcodeResponse:
        """QR-код поставки."""
        return self.get(
            f"/api/v3/supplies/{supply_id}/barcode",
            params={"type": barcode_type},
            response_model=BarcodeResponse,
        )

    def get_supply_boxes(self, supply_id: str) -> SupplyBoxesResponse:
        """Список коробок поставки."""
        return self.get(
            f"/api/v3/supplies/{supply_id}/trbx",
            response_model=SupplyBoxesResponse,
        )

    def add_boxes_to_supply(self, supply_id: str, amount: int) -> TrbxIdsResponse:
        """Добавление коробок в поставку."""
        return self.post(
            f"/api/v3/supplies/{supply_id}/trbx",
            json={"amount": amount},
            response_model=TrbxIdsResponse,
        )

    def delete_boxes_from_supply(self, supply_id: str, trbx_ids: list[str]) -> None:
        """Удаление коробок из поставки."""
        self.delete(
            f"/api/v3/supplies/{supply_id}/trbx",
            json={"trbxIds": trbx_ids},
        )

    def get_supply_box_stickers(
        self,
        supply_id: str,
        trbx_ids: list[str],
        *,
        sticker_type: str = "svg",
    ) -> TrbxStickersResponse:
        """Стикеры коробок поставки."""
        return self.post(
            f"/api/v3/supplies/{supply_id}/trbx/stickers",
            params={"type": sticker_type},
            json={"trbxIds": trbx_ids},
            response_model=TrbxStickersResponse,
        )

    # --- Пропуска ---

    def get_passes_offices(self) -> list[PassOffice]:
        """Офисы, требующие пропуск."""
        return self.get(
            "/api/v3/passes/offices",
            response_model=list[PassOffice],
        )

    def get_passes(self) -> list[Pass]:
        """Список пропусков."""
        return self.get(
            "/api/v3/passes",
            response_model=list[Pass],
        )

    def create_pass(
        self,
        first_name: str,
        last_name: str,
        car_model: str,
        car_number: str,
        office_id: int,
    ) -> PassCreateResponse:
        """Создание пропуска."""
        return self.post(
            "/api/v3/passes",
            json={
                "firstName": first_name,
                "lastName": last_name,
                "carModel": car_model,
                "carNumber": car_number,
                "officeId": office_id,
            },
            response_model=PassCreateResponse,
        )

    def update_pass(
        self,
        pass_id: int,
        first_name: str,
        last_name: str,
        car_model: str,
        car_number: str,
        office_id: int,
    ) -> None:
        """Обновление пропуска."""
        self.put(
            f"/api/v3/passes/{pass_id}",
            json={
                "firstName": first_name,
                "lastName": last_name,
                "carModel": car_model,
                "carNumber": car_number,
                "officeId": office_id,
            },
        )

    def delete_pass(self, pass_id: int) -> None:
        """Удаление пропуска."""
        self.delete(f"/api/v3/passes/{pass_id}")
