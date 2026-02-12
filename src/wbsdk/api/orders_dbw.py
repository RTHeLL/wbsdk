"""API заказов DBW (доставка курьером WB)."""

from typing import Any

from wbsdk.api.base import BaseAPI
from wbsdk.schemas.orders_dbw import OrdersListResponse, OrdersNewResponse


class OrdersDBWAPI(BaseAPI):
    """API сборочных заданий и метаданных DBW."""

    def __init__(self, client: Any, base_url: str):
        super().__init__(client, base_url, domain="marketplace")

    def get_new_orders(self) -> OrdersNewResponse:
        """Новые сборочные задания DBW."""
        return self.get(
            "/api/v3/dbw/orders/new",
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
        """Завершённые сборочные задания за период (макс. 30 дней)."""
        return self.get(
            "/api/v3/dbw/orders",
            params={
                "dateFrom": date_from,
                "dateTo": date_to,
                "limit": limit,
                "next": next_cursor,
            },
            response_model=OrdersListResponse,
        )

    def get_orders_delivery_date(self, payload: dict[str, Any]) -> Any:
        """Дата и время доставки по заказам."""
        return self.post("/api/v3/dbw/orders/delivery-date", json=payload)

    def get_orders_status(self, order_ids: list[int]) -> Any:
        """Статусы сборочных заданий DBW."""
        return self.post(
            "/api/v3/dbw/orders/status",
            json={"orders": order_ids},
        )

    def confirm_order(self, order_id: int) -> None:
        """Перевести сборочное задание на сборку."""
        self.patch(f"/api/v3/dbw/orders/{order_id}/confirm")

    def get_orders_stickers(
        self,
        order_ids: list[int],
        *,
        sticker_type: str = "svg",
        width: int = 58,
        height: int = 40,
    ) -> Any:
        """Стикеры для заказов DBW."""
        return self.post(
            "/api/v3/dbw/orders/stickers",
            params={"type": sticker_type, "width": width, "height": height},
            json={"orders": order_ids},
        )

    def assemble_order(self, order_id: int) -> None:
        """Перевести сборочное задание в доставку (готово к передаче курьеру)."""
        self.patch(f"/api/v3/dbw/orders/{order_id}/assemble")

    def get_courier_orders(self, date: str) -> Any:
        """Заказы, переданные курьеру. date: ГГГГ-ММ-ДД."""
        return self.get(
            "/api/v3/dbw/orders/courier",
            params={"date": date},
        )

    def cancel_order(self, order_id: int) -> None:
        """Отменить сборочное задание DBW."""
        self.patch(f"/api/v3/dbw/orders/{order_id}/cancel")

    def get_order_meta(self, order_id: int) -> Any:
        """Метаданные одного заказа DBW."""
        return self.get(f"/api/v3/dbw/orders/{order_id}/meta")

    def delete_order_meta(self, order_id: int, *, key: str | None = None) -> None:
        """Удалить метаданные заказа DBW."""
        params = {}
        if key:
            params["key"] = key
        self.delete(f"/api/v3/dbw/orders/{order_id}/meta", params=params or None)

    def add_order_sgtin(self, order_id: int, sgtins: list[str]) -> None:
        """Добавить коды маркировки к заказу DBW."""
        self.put(f"/api/v3/dbw/orders/{order_id}/meta/sgtin", json={"sgtins": sgtins})

    def add_order_uin(self, order_id: int, uin: str) -> None:
        """Добавить УИН к заказу DBW."""
        self.put(f"/api/v3/dbw/orders/{order_id}/meta/uin", json={"uin": uin})

    def add_order_imei(self, order_id: int, imei: str) -> None:
        """Добавить IMEI к заказу DBW."""
        self.put(f"/api/v3/dbw/orders/{order_id}/meta/imei", json={"imei": imei})

    def add_order_gtin(self, order_id: int, gtin: str) -> None:
        """Добавить GTIN к заказу DBW."""
        self.put(f"/api/v3/dbw/orders/{order_id}/meta/gtin", json={"gtin": gtin})
