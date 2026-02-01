"""API аналитики, воронки продаж и поисковых запросов."""

from typing import Any

from wbsdk.api.base import BaseAPI
from wbsdk.schemas.analytics import (
    NmReportCreateResponse,
    NmReportRetryResponse,
    NmReportsListResponse,
    SalesFunnelGroupedResponse,
    SalesFunnelHistoryResponse,
    SalesFunnelProductsResponse,
    SearchReportResponse,
    StocksGroupsResponse,
    StocksProductsResponse,
)


class AnalyticsAPI(BaseAPI):
    """API аналитики продавца."""

    def __init__(self, client: Any, base_url: str):
        super().__init__(client, base_url, domain="analytics")

    # --- Воронка продаж ---

    def get_sales_funnel_products(
        self,
        selected_period: dict,
        *,
        past_period: dict | None = None,
        nm_ids: list[int] | None = None,
        brand_names: list[str] | None = None,
        subject_ids: list[int] | None = None,
        tag_ids: list[int] | None = None,
        skip_deleted_nm: bool = False,
        order_by: dict | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> SalesFunnelProductsResponse:
        """Статистика по карточкам за период."""
        payload: dict[str, Any] = {
            "selectedPeriod": selected_period,
            "limit": limit,
            "offset": offset,
            "skipDeletedNm": skip_deleted_nm,
        }
        if past_period:
            payload["pastPeriod"] = past_period
        if nm_ids is not None:
            payload["nmIds"] = nm_ids
        if brand_names is not None:
            payload["brandNames"] = brand_names
        if subject_ids is not None:
            payload["subjectIds"] = subject_ids
        if tag_ids is not None:
            payload["tagIds"] = tag_ids
        if order_by:
            payload["orderBy"] = order_by
        return self.post(
            "/api/analytics/v3/sales-funnel/products",
            json=payload,
            response_model=SalesFunnelProductsResponse,
        )

    def get_sales_funnel_products_history(
        self,
        selected_period: dict,
        nm_ids: list[int],
        *,
        skip_deleted_nm: bool = False,
        aggregation_level: str = "day",
    ) -> SalesFunnelHistoryResponse:
        """Статистика по карточкам по дням/неделям (макс. 20 nm_ids, 7 дней)."""
        return self.post(
            "/api/analytics/v3/sales-funnel/products/history",
            json={
                "selectedPeriod": selected_period,
                "nmIds": nm_ids,
                "skipDeletedNm": skip_deleted_nm,
                "aggregationLevel": aggregation_level,
            },
            response_model=SalesFunnelHistoryResponse,
        )

    def get_sales_funnel_grouped_history(
        self,
        selected_period: dict,
        *,
        brand_names: list[str] | None = None,
        subject_ids: list[int] | None = None,
        tag_ids: list[int] | None = None,
        skip_deleted_nm: bool = False,
        aggregation_level: str = "day",
    ) -> SalesFunnelGroupedResponse:
        """Статистика по группам (субъект, бренд, тег) по дням."""
        payload: dict[str, Any] = {
            "selectedPeriod": selected_period,
            "skipDeletedNm": skip_deleted_nm,
            "aggregationLevel": aggregation_level,
        }
        if brand_names is not None:
            payload["brandNames"] = brand_names
        if subject_ids is not None:
            payload["subjectIds"] = subject_ids
        if tag_ids is not None:
            payload["tagIds"] = tag_ids
        return self.post(
            "/api/analytics/v3/sales-funnel/grouped/history",
            json=payload,
            response_model=SalesFunnelGroupedResponse,
        )

    # --- Поисковые запросы (требует Jam) ---

    def get_search_report(
        self,
        current_period: dict,
        order_by: dict,
        limit: int,
        offset: int,
        *,
        past_period: dict | None = None,
        nm_ids: list[int] | None = None,
        subject_ids: list[int] | None = None,
        brand_names: list[str] | None = None,
        tag_ids: list[int] | None = None,
        position_cluster: str = "all",
        include_substituted_skus: bool = True,
        include_search_texts: bool = True,
    ) -> SearchReportResponse:
        """Основная страница отчёта по поисковым запросам."""
        payload: dict[str, Any] = {
            "currentPeriod": current_period,
            "orderBy": order_by,
            "limit": limit,
            "offset": offset,
            "positionCluster": position_cluster,
            "includeSubstitutedSKUs": include_substituted_skus,
            "includeSearchTexts": include_search_texts,
        }
        if past_period:
            payload["pastPeriod"] = past_period
        if nm_ids is not None:
            payload["nmIds"] = nm_ids
        if subject_ids is not None:
            payload["subjectIds"] = subject_ids
        if brand_names is not None:
            payload["brandNames"] = brand_names
        if tag_ids is not None:
            payload["tagIds"] = tag_ids
        return self.post(
            "/api/v2/search-report/report",
            json=payload,
            response_model=SearchReportResponse,
        )

    # --- Отчёты по остаткам ---

    def get_stocks_groups(
        self,
        current_period: dict,
        stock_type: str,
        skip_deleted_nm: bool,
        availability_filters: list[str],
        order_by: dict,
        offset: int,
        *,
        nm_ids: list[int] | None = None,
        subject_ids: list[int] | None = None,
        brand_names: list[str] | None = None,
        tag_ids: list[int] | None = None,
        limit: int = 100,
    ) -> StocksGroupsResponse:
        """Данные по остаткам по группам. stock_type: '' | 'wb' | 'mp'."""
        payload: dict[str, Any] = {
            "currentPeriod": current_period,
            "stockType": stock_type,
            "skipDeletedNm": skip_deleted_nm,
            "availabilityFilters": availability_filters,
            "orderBy": order_by,
            "limit": limit,
            "offset": offset,
        }
        if nm_ids is not None:
            payload["nmIDs"] = nm_ids
        if subject_ids is not None:
            payload["subjectIDs"] = subject_ids
        if brand_names is not None:
            payload["brandNames"] = brand_names
        if tag_ids is not None:
            payload["tagIDs"] = tag_ids
        return self.post(
            "/api/v2/stocks-report/products/groups",
            json=payload,
            response_model=StocksGroupsResponse,
        )

    def get_stocks_products(
        self,
        current_period: dict,
        stock_type: str,
        skip_deleted_nm: bool,
        order_by: dict,
        availability_filters: list[str],
        offset: int,
        *,
        nm_ids: list[int] | None = None,
        subject_id: int | None = None,
        brand_name: str | None = None,
        tag_id: int | None = None,
        limit: int = 100,
    ) -> StocksProductsResponse:
        """Данные по остаткам по товарам."""
        payload: dict[str, Any] = {
            "currentPeriod": current_period,
            "stockType": stock_type,
            "skipDeletedNm": skip_deleted_nm,
            "orderBy": order_by,
            "availabilityFilters": availability_filters,
            "limit": limit,
            "offset": offset,
        }
        if nm_ids is not None:
            payload["nmIDs"] = nm_ids
        if subject_id is not None:
            payload["subjectID"] = subject_id
        if brand_name is not None:
            payload["brandName"] = brand_name
        if tag_id is not None:
            payload["tagID"] = tag_id
        return self.post(
            "/api/v2/stocks-report/products/products",
            json=payload,
            response_model=StocksProductsResponse,
        )

    # --- CSV отчёты ---

    def create_nm_report(
        self,
        report_id: str,
        report_type: str,
        params: dict,
        *,
        user_report_name: str | None = None,
    ) -> NmReportCreateResponse:
        """Создание задачи на генерацию CSV отчёта (макс. 20 в день)."""
        payload: dict[str, Any] = {"id": report_id, "reportType": report_type, "params": params}
        if user_report_name:
            payload["userReportName"] = user_report_name
        return self.post(
            "/api/v2/nm-report/downloads",
            json=payload,
            response_model=NmReportCreateResponse,
        )

    def get_nm_reports_list(
        self, *, download_ids: list[str] | None = None
    ) -> NmReportsListResponse:
        """Список отчётов и их статусов."""
        params: dict[str, Any] = {}
        if download_ids:
            params["filter[downloadIds]"] = download_ids
        return self.get(
            "/api/v2/nm-report/downloads",
            params=params or None,
            response_model=NmReportsListResponse,
        )

    def retry_nm_report(self, download_id: str) -> NmReportRetryResponse:
        """Повторная генерация отчёта при статусе FAILED."""
        return self.post(
            "/api/v2/nm-report/downloads/retry",
            json={"downloadId": download_id},
            response_model=NmReportRetryResponse,
        )

    def get_nm_report_file(self, download_id: str) -> bytes:
        """Скачивание готового отчёта (доступен 48 ч)."""
        return self._client.request_raw(
            "GET",
            f"{self._base_url}/api/v2/nm-report/downloads/file/{download_id}",
            domain="analytics",
        )
