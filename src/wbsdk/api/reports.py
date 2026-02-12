"""API отчётов поставок (statistics-api): поставки, остатки, заказы, продажи."""

from typing import Any

from wbsdk.api.base import BaseAPI


class ReportsAPI(BaseAPI):
    """API отчётов: поставки, остатки, заказы, продажи (statistics-api)."""

    def __init__(self, client: Any, base_url: str):
        super().__init__(client, base_url, domain="statistics")

    def get_incomes(self, date_from: str, date_to: str) -> Any:
        """Поставки. date в формате ГГГГ-ММ-ДД."""
        return self.get(
            "/api/v1/supplier/incomes",
            params={"dateFrom": date_from, "dateTo": date_to},
        )

    def get_stocks(self, date_from: str, date_to: str) -> Any:
        """Остатки. date в формате ГГГГ-ММ-ДД."""
        return self.get(
            "/api/v1/supplier/stocks",
            params={"dateFrom": date_from, "dateTo": date_to},
        )

    def get_orders(
        self,
        date_from: str,
        date_to: str,
        *,
        flag: int = 0,
    ) -> Any:
        """Заказы. date в формате ГГГГ-ММ-ДД."""
        return self.get(
            "/api/v1/supplier/orders",
            params={"dateFrom": date_from, "dateTo": date_to, "flag": flag},
        )

    def get_sales(
        self,
        date_from: str,
        date_to: str,
        *,
        flag: int = 0,
    ) -> Any:
        """Продажи. date в формате ГГГГ-ММ-ДД."""
        return self.get(
            "/api/v1/supplier/sales",
            params={"dateFrom": date_from, "dateTo": date_to, "flag": flag},
        )

    def get_report_detail_by_period(
        self,
        date_from: str,
        date_to: str,
        *,
        limit: int = 100000,
        rrdid: int = 0,
        period: str = "weekly",
    ) -> Any:
        """Отчёт о продажах по реализации (statistics-api). date в формате RFC3339."""
        return self.get(
            "/api/v5/supplier/reportDetailByPeriod",
            params={
                "dateFrom": date_from,
                "dateTo": date_to,
                "limit": limit,
                "rrdid": rrdid,
                "period": period,
            },
        )
