"""API заказов DBS (витрина)."""

from typing import Any

from wbsdk.api.base import BaseAPI
from wbsdk.schemas.orders_dbs import OrdersListResponse, OrdersNewResponse


class OrdersDBSAPI(BaseAPI):
    """API сборочных заданий и метаданных DBS."""

    def __init__(self, client: Any, base_url: str):
        super().__init__(client, base_url, domain="marketplace")

    # --- /api/v3/dbs/ ---

    def get_new_orders(self) -> OrdersNewResponse:
        """Новые сборочные задания DBS."""
        return self.get(
            "/api/v3/dbs/orders/new",
            response_model=OrdersNewResponse,
        )

    def get_orders(
        self,
        date_from: int,
        date_to: int,
        *,
        limit: int = 100,
        next_cursor: int = 0,
    ) -> OrdersListResponse:
        """Заказы DBS за период (макс. 30 дней)."""
        return self.get(
            "/api/v3/dbs/orders",
            params={
                "dateFrom": date_from,
                "dateTo": date_to,
                "limit": limit,
                "next": next_cursor,
            },
            response_model=OrdersListResponse,
        )

    def get_groups_info(self, payload: dict[str, Any]) -> Any:
        """Информация по группам заказов DBS."""
        return self.post("/api/v3/dbs/groups/info", json=payload)

    def get_orders_client(self, order_ids: list[int]) -> Any:
        """Информация о покупателях по заказам DBS."""
        return self.post(
            "/api/v3/dbs/orders/client",
            json={"orders": order_ids},
        )

    def get_orders_delivery_date(self, payload: dict[str, Any]) -> Any:
        """Дата и время доставки по заказам DBS."""
        return self.post("/api/v3/dbs/orders/delivery-date", json=payload)

    def get_orders_status(self, order_ids: list[int]) -> Any:
        """Статусы сборочных заданий DBS (v3)."""
        return self.post(
            "/api/v3/dbs/orders/status",
            json={"orders": order_ids},
        )

    def cancel_order(self, order_id: int) -> None:
        """Отменить сборочное задание DBS."""
        self.patch(f"/api/v3/dbs/orders/{order_id}/cancel")

    def confirm_order(self, order_id: int) -> None:
        """Перевести сборочное задание на сборку."""
        self.patch(f"/api/v3/dbs/orders/{order_id}/confirm")

    def deliver_order(self, order_id: int) -> None:
        """Перевести сборочное задание в доставку."""
        self.patch(f"/api/v3/dbs/orders/{order_id}/deliver")

    def receive_order(self, order_id: int) -> None:
        """Заказ получен покупателем."""
        self.patch(f"/api/v3/dbs/orders/{order_id}/receive")

    def reject_order(self, order_id: int) -> None:
        """Покупатель отказался от заказа."""
        self.patch(f"/api/v3/dbs/orders/{order_id}/reject")

    def get_order_meta(self, order_id: int) -> Any:
        """Метаданные одного заказа DBS."""
        return self.get(f"/api/v3/dbs/orders/{order_id}/meta")

    def add_order_sgtin(self, order_id: int, sgtins: list[str]) -> None:
        """Добавить коды маркировки к заказу DBS."""
        self.put(f"/api/v3/dbs/orders/{order_id}/meta/sgtin", json={"sgtins": sgtins})

    def add_order_uin(self, order_id: int, uin: str) -> None:
        """Добавить УИН к заказу DBS."""
        self.put(f"/api/v3/dbs/orders/{order_id}/meta/uin", json={"uin": uin})

    def add_order_imei(self, order_id: int, imei: str) -> None:
        """Добавить IMEI к заказу DBS."""
        self.put(f"/api/v3/dbs/orders/{order_id}/meta/imei", json={"imei": imei})

    def add_order_gtin(self, order_id: int, gtin: str) -> None:
        """Добавить GTIN к заказу DBS."""
        self.put(f"/api/v3/dbs/orders/{order_id}/meta/gtin", json={"gtin": gtin})

    # --- /api/marketplace/v3/dbs/ ---

    def get_orders_b2b_info(self, order_ids: list[int]) -> Any:
        """Информация о B2B-покупателях по заказам."""
        return self.post(
            "/api/marketplace/v3/dbs/orders/b2b/info",
            json={"orders": order_ids},
        )

    def get_orders_status_info(self, order_ids: list[int]) -> Any:
        """Статусы сборочных заданий DBS (marketplace)."""
        return self.post(
            "/api/marketplace/v3/dbs/orders/status/info",
            json={"orders": order_ids},
        )

    def cancel_orders_status(self, order_ids: list[int]) -> Any:
        """Отменить сборочные задания (batch)."""
        return self.post(
            "/api/marketplace/v3/dbs/orders/status/cancel",
            json={"orders": order_ids},
        )

    def confirm_orders_status(self, order_ids: list[int]) -> Any:
        """Перевести сборочные задания на сборку (batch)."""
        return self.post(
            "/api/marketplace/v3/dbs/orders/status/confirm",
            json={"orders": order_ids},
        )

    def deliver_orders_status(self, order_ids: list[int]) -> Any:
        """Перевести сборочные задания в доставку (batch)."""
        return self.post(
            "/api/marketplace/v3/dbs/orders/status/deliver",
            json={"orders": order_ids},
        )

    def receive_orders_status(self, order_ids: list[int]) -> Any:
        """Заказы получены покупателем (batch)."""
        return self.post(
            "/api/marketplace/v3/dbs/orders/status/receive",
            json={"orders": order_ids},
        )

    def reject_orders_status(self, order_ids: list[int]) -> Any:
        """Покупатель отказался от заказов (batch)."""
        return self.post(
            "/api/marketplace/v3/dbs/orders/status/reject",
            json={"orders": order_ids},
        )

    def get_orders_meta_info(self, order_ids: list[int]) -> Any:
        """Метаданные заказов DBS (batch)."""
        return self.post(
            "/api/marketplace/v3/dbs/orders/meta/info",
            json={"orders": order_ids},
        )

    def delete_orders_meta(self, payload: dict[str, Any]) -> Any:
        """Удалить метаданные заказов DBS."""
        return self.post(
            "/api/marketplace/v3/dbs/orders/meta/delete",
            json=payload,
        )

    def add_orders_meta_sgtin(self, payload: dict[str, Any]) -> Any:
        """Добавить коды маркировки к заказам DBS (batch)."""
        return self.post(
            "/api/marketplace/v3/dbs/orders/meta/sgtin",
            json=payload,
        )

    def add_orders_meta_uin(self, payload: dict[str, Any]) -> Any:
        """Добавить УИН к заказам DBS (batch)."""
        return self.post(
            "/api/marketplace/v3/dbs/orders/meta/uin",
            json=payload,
        )

    def add_orders_meta_imei(self, payload: dict[str, Any]) -> Any:
        """Добавить IMEI к заказам DBS (batch)."""
        return self.post(
            "/api/marketplace/v3/dbs/orders/meta/imei",
            json=payload,
        )

    def add_orders_meta_gtin(self, payload: dict[str, Any]) -> Any:
        """Добавить GTIN к заказам DBS (batch)."""
        return self.post(
            "/api/marketplace/v3/dbs/orders/meta/gtin",
            json=payload,
        )

    def add_orders_meta_customs_declaration(self, payload: dict[str, Any]) -> Any:
        """Добавить номер ГТД к заказам DBS (batch)."""
        return self.post(
            "/api/marketplace/v3/dbs/orders/meta/customs-declaration",
            json=payload,
        )
