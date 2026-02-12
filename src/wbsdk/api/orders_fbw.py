"""API поставок FBW (склад WB)."""

from typing import Any

from wbsdk.api.base import BaseAPI


class OrdersFBWAPI(BaseAPI):
    """API информации для формирования поставок и информации о поставках FBW."""

    def __init__(self, client: Any, base_url: str):
        super().__init__(client, base_url, domain="supplies")

    def get_acceptance_coefficients(
        self,
        *,
        warehouse_ids: str | None = None,
    ) -> Any:
        """Коэффициенты приёмки (deprecated: используйте tariffs.get_acceptance_coefficients)."""
        params = {}
        if warehouse_ids is not None:
            params["warehouseIDs"] = warehouse_ids
        return self.get(
            "/api/v1/acceptance/coefficients",
            params=params or None,
        )

    def get_acceptance_options(
        self,
        goods: list[dict[str, Any]],
        *,
        warehouse_id: int | None = None,
    ) -> Any:
        """Опции приёмки: склады и типы упаковки по баркоду и количеству."""
        params = {}
        if warehouse_id is not None:
            params["warehouseID"] = warehouse_id
        return self.post(
            "/api/v1/acceptance/options",
            params=params or None,
            json=goods,
        )

    def get_warehouses(self) -> Any:
        """Список складов WB для FBW."""
        return self.get("/api/v1/warehouses")

    def get_transit_tariffs(self) -> Any:
        """Транзитные направления."""
        return self.get("/api/v1/transit-tariffs")

    def get_supplies(
        self,
        payload: dict[str, Any],
        *,
        limit: int = 1000,
        offset: int = 0,
    ) -> Any:
        """Список поставок FBW."""
        return self.post(
            "/api/v1/supplies",
            params={"limit": limit, "offset": offset},
            json=payload,
        )

    def get_supply_details(
        self,
        supply_id: int,
        *,
        is_preorder_id: bool = False,
    ) -> Any:
        """Детали поставки по ID поставки или заказа."""
        return self.get(
            f"/api/v1/supplies/{supply_id}",
            params={"isPreorderID": is_preorder_id},
        )

    def get_supply_goods(
        self,
        supply_id: int,
        *,
        limit: int = 100,
        offset: int = 0,
        is_preorder_id: bool = False,
    ) -> Any:
        """Товары в поставке."""
        return self.get(
            f"/api/v1/supplies/{supply_id}/goods",
            params={
                "limit": limit,
                "offset": offset,
                "isPreorderID": is_preorder_id,
            },
        )

    def get_supply_package(
        self,
        supply_id: int,
        *,
        is_preorder_id: bool = False,
    ) -> Any:
        """Упаковка поставки."""
        return self.get(
            f"/api/v1/supplies/{supply_id}/package",
            params={"isPreorderID": is_preorder_id},
        )
