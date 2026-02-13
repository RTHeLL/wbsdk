"""API тарифов: комиссии, короба, паллеты, приёмка, возврат (common-api)."""

import inspect
from typing import Any

from wbsdk.api.base import BaseAPI
from wbsdk.schemas.tariffs import TariffsResponse


class TariffsAPI(BaseAPI):
    """API комиссий и тарифов на остаток/возврат."""

    def __init__(self, client: Any, base_url: str):
        super().__init__(client, base_url, domain="common")

    def get_commission(
        self,
        *,
        locale: str = "ru",
    ) -> TariffsResponse:
        """Комиссия по категориям товаров. locale: ru, en, zh."""
        return self.get(
            "/api/v1/tariffs/commission",
            params={"locale": locale},
            response_model=TariffsResponse,
        )

    def get_tariffs_box(self, date: str) -> TariffsResponse:
        """Тарифы для коробов. date в формате ГГГГ-ММ-ДД."""
        return self.get(
            "/api/v1/tariffs/box",
            params={"date": date},
            response_model=TariffsResponse,
        )

    def get_tariffs_pallet(self, date: str) -> TariffsResponse:
        """Тарифы для монопаллет. date в формате ГГГГ-ММ-ДД."""
        return self.get(
            "/api/v1/tariffs/pallet",
            params={"date": date},
            response_model=TariffsResponse,
        )

    def get_tariffs_return(self, date: str) -> TariffsResponse:
        """Тарифы на возврат. date в формате ГГГГ-ММ-ДД."""
        return self.get(
            "/api/v1/tariffs/return",
            params={"date": date},
            response_model=TariffsResponse,
        )

    def get_acceptance_coefficients(
        self,
        *,
        warehouse_ids: str | None = None,
    ) -> list[dict[str, Any]] | Any:
        """Тарифы на поставку по складам на ближайшие 14 дней."""
        params: dict[str, Any] = {}
        if warehouse_ids is not None:
            params["warehouseIDs"] = warehouse_ids
        result = self.get(
            "/api/tariffs/v1/acceptance/coefficients",
            params=params or None,
        )
        if inspect.iscoroutine(result):

            async def _await_and_normalize() -> list[dict[str, Any]]:
                raw = await result
                return raw if isinstance(raw, list) else []

            return _await_and_normalize()
        return result if isinstance(result, list) else []
