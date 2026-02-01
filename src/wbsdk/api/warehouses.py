"""API складов продавца и остатков DBW."""

from typing import Any

from wbsdk.api.base import BaseAPI


class WarehousesAPI(BaseAPI):
    """API для работы со складами продавца (DBW)."""

    def __init__(self, client: Any, base_url: str):
        super().__init__(client, base_url, domain="marketplace")

    def get_offices(self) -> Any:
        """Список офисов для привязки к складу."""
        return self.get("/api/v3/offices")

    def get_warehouses(self) -> Any:
        """Список складов продавца."""
        return self.get("/api/v3/warehouses")

    def create_warehouse(self, name: str, office_id: int) -> Any:
        """Создание склада."""
        return self.post("/api/v3/warehouses", json={"name": name, "officeId": office_id})

    def update_warehouse(self, warehouse_id: int, name: str, office_id: int) -> None:
        """Обновление склада."""
        self.put(
            f"/api/v3/warehouses/{warehouse_id}",
            json={"name": name, "officeId": office_id},
        )

    def delete_warehouse(self, warehouse_id: int) -> None:
        """Удаление склада."""
        self.delete(f"/api/v3/warehouses/{warehouse_id}")

    def get_warehouse_contacts(self, warehouse_id: int) -> Any:
        """Контакты склада (только для DBW)."""
        return self.get(f"/api/v3/dbw/warehouses/{warehouse_id}/contacts")

    def update_warehouse_contacts(
        self,
        warehouse_id: int,
        contacts: list[dict],
    ) -> None:
        """Обновление контактов склада (макс. 5)."""
        self.put(
            f"/api/v3/dbw/warehouses/{warehouse_id}/contacts",
            json={"contacts": contacts},
        )

    def update_stocks(self, warehouse_id: int, stocks: list[dict]) -> None:
        """Обновление остатков на складе. stocks: [{chrtId, sku, amount}, ...]."""
        self.put(
            f"/api/v3/stocks/{warehouse_id}",
            json={"stocks": stocks},
        )

    def delete_stocks(
        self,
        warehouse_id: int,
        chrt_ids: list[int],
        *,
        skus: list[str] | None = None,
    ) -> None:
        """Удаление остатков (необратимо)."""
        payload: dict[str, Any] = {"chrtIds": chrt_ids}
        if skus:
            payload["skus"] = skus
        self.delete(f"/api/v3/stocks/{warehouse_id}", json=payload)

    def get_stocks(
        self,
        warehouse_id: int,
        *,
        skip: int = 0,
        take: int = 1000,
    ) -> Any:
        """Получение остатков склада."""
        return self.post(
            f"/api/v3/stocks/{warehouse_id}",
            json={"skip": skip, "take": take},
        )
