"""API заказов самовывоза (Click&Collect)."""

from typing import Any

from wbsdk.api.base import BaseAPI
from wbsdk.schemas.click_collect import OrdersListResponse, OrdersNewResponse


class ClickCollectAPI(BaseAPI):
    """API сборочных заданий и метаданных самовывоза."""

    def __init__(self, client: Any, base_url: str):
        super().__init__(client, base_url, domain="marketplace")

    def get_new_orders(self) -> OrdersNewResponse:
        """Новые сборочные задания самовывоза."""
        return self.get(
            "/api/v3/click-collect/orders/new",
            response_model=OrdersNewResponse,
        )

    def confirm_order(self, order_id: int) -> None:
        """Перевести сборочное задание на сборку."""
        self.patch(f"/api/v3/click-collect/orders/{order_id}/confirm")

    def prepare_order(self, order_id: int) -> None:
        """Сборочное задание готово к выдаче."""
        self.patch(f"/api/v3/click-collect/orders/{order_id}/prepare")

    def get_orders_client(self, order_ids: list[int]) -> Any:
        """Информация о покупателе по заказам."""
        return self.post(
            "/api/v3/click-collect/orders/client",
            json={"orders": order_ids},
        )

    def get_orders_client_identity(self, order_id: int, identity: str) -> Any:
        """Проверить, что заказ принадлежит покупателю (по коду/документу)."""
        return self.post(
            "/api/v3/click-collect/orders/client/identity",
            json={"orderId": order_id, "identity": identity},
        )

    def receive_order(self, order_id: int) -> None:
        """Заказ получен покупателем."""
        self.patch(f"/api/v3/click-collect/orders/{order_id}/receive")

    def reject_order(self, order_id: int) -> None:
        """Покупатель отказался от заказа."""
        self.patch(f"/api/v3/click-collect/orders/{order_id}/reject")

    def get_orders_status(self, order_ids: list[int]) -> Any:
        """Статусы сборочных заданий самовывоза."""
        return self.post(
            "/api/v3/click-collect/orders/status",
            json={"orders": order_ids},
        )

    def get_orders(
        self,
        date_from: int,
        date_to: int,
        *,
        limit: int = 100,
        next_cursor: int = 0,
    ) -> OrdersListResponse:
        """Список заказов самовывоза за период."""
        return self.get(
            "/api/v3/click-collect/orders",
            params={
                "dateFrom": date_from,
                "dateTo": date_to,
                "limit": limit,
                "next": next_cursor,
            },
            response_model=OrdersListResponse,
        )

    def cancel_order(self, order_id: int) -> None:
        """Отменить сборочное задание самовывоза."""
        self.patch(f"/api/v3/click-collect/orders/{order_id}/cancel")

    def get_order_meta(self, order_id: int) -> Any:
        """Метаданные одного заказа самовывоза."""
        return self.get(f"/api/v3/click-collect/orders/{order_id}/meta")

    def add_order_sgtin(self, order_id: int, sgtins: list[str]) -> None:
        """Добавить коды маркировки к заказу."""
        self.put(
            f"/api/v3/click-collect/orders/{order_id}/meta/sgtin",
            json={"sgtins": sgtins},
        )

    def add_order_uin(self, order_id: int, uin: str) -> None:
        """Добавить УИН к заказу."""
        self.put(
            f"/api/v3/click-collect/orders/{order_id}/meta/uin",
            json={"uin": uin},
        )

    def add_order_imei(self, order_id: int, imei: str) -> None:
        """Добавить IMEI к заказу."""
        self.put(
            f"/api/v3/click-collect/orders/{order_id}/meta/imei",
            json={"imei": imei},
        )

    def add_order_gtin(self, order_id: int, gtin: str) -> None:
        """Добавить GTIN к заказу."""
        self.put(
            f"/api/v3/click-collect/orders/{order_id}/meta/gtin",
            json={"gtin": gtin},
        )
