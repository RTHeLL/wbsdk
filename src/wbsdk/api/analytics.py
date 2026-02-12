"""API аналитики, воронки продаж и поисковых запросов."""

from typing import Any

from wbsdk.api.base import BaseAPI
from wbsdk.schemas.analytics import (
    AnalyticsDataResponse,
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

    # --- Поисковые запросы: таблицы и товар ---

    def get_search_report_table_groups(self, payload: dict[str, Any]) -> AnalyticsDataResponse:
        """Пагинация по группам в отчёте по поисковым запросам."""
        return self.post(
            "/api/v2/search-report/table/groups",
            json=payload,
            response_model=AnalyticsDataResponse,
        )

    def get_search_report_table_details(
        self, payload: dict[str, Any]
    ) -> AnalyticsDataResponse:
        """Пагинация по товарам в группе в отчёте по поисковым запросам."""
        return self.post(
            "/api/v2/search-report/table/details",
            json=payload,
            response_model=AnalyticsDataResponse,
        )

    def get_search_report_product_search_texts(
        self, payload: dict[str, Any]
    ) -> AnalyticsDataResponse:
        """Топ поисковых запросов по товару."""
        return self.post(
            "/api/v2/search-report/product/search-texts",
            json=payload,
            response_model=AnalyticsDataResponse,
        )

    def get_search_report_product_orders(
        self, payload: dict[str, Any]
    ) -> AnalyticsDataResponse:
        """Заказы и позиции по поисковым запросам товара."""
        return self.post(
            "/api/v2/search-report/product/orders",
            json=payload,
            response_model=AnalyticsDataResponse,
        )

    # --- История остатков: офисы и размеры ---

    def get_stocks_report_offices(
        self, payload: dict[str, Any]
    ) -> AnalyticsDataResponse:
        """Данные по остаткам по складам."""
        return self.post(
            "/api/v2/stocks-report/offices",
            json=payload,
            response_model=AnalyticsDataResponse,
        )

    def get_stocks_report_products_sizes(
        self, payload: dict[str, Any]
    ) -> AnalyticsDataResponse:
        """Данные по остаткам по размерам товара."""
        return self.post(
            "/api/v2/stocks-report/products/sizes",
            json=payload,
            response_model=AnalyticsDataResponse,
        )

    # --- Отчёты (seller-analytics) ---

    def get_excise_report(self, params: dict[str, Any]) -> Any:
        """Отчёт по акцизам."""
        return self.get("/api/v1/analytics/excise-report", params=params)

    def create_warehouse_remains_task(self, payload: dict[str, Any]) -> Any:
        """Создать задачу отчёта остатков на складе."""
        return self.post("/api/v1/warehouse_remains", json=payload)

    def get_warehouse_remains_task_status(self, task_id: int) -> Any:
        """Статус задачи остатков на складе."""
        return self.get(f"/api/v1/warehouse_remains/tasks/{task_id}/status")

    def get_warehouse_remains_task_download(self, task_id: int) -> bytes:
        """Скачать отчёт остатков на складе."""
        return self._client.request_raw(
            "GET",
            f"{self._base_url}/api/v1/warehouse_remains/tasks/{task_id}/download",
            domain="analytics",
        )

    def get_measurement_penalties(self, params: dict[str, Any]) -> Any:
        """Штрафы по замерам."""
        return self.get("/api/analytics/v1/measurement-penalties", params=params)

    def get_warehouse_measurements(self, params: dict[str, Any]) -> Any:
        """Замеры на складе."""
        return self.get("/api/analytics/v1/warehouse-measurements", params=params)

    def get_deductions(self, params: dict[str, Any]) -> Any:
        """Удержания."""
        return self.get("/api/analytics/v1/deductions", params=params)

    def get_antifraud_details(self, params: dict[str, Any]) -> Any:
        """Детали антифрода."""
        return self.get("/api/v1/analytics/antifraud-details", params=params)

    def get_goods_labeling(self, params: dict[str, Any]) -> Any:
        """Маркировка товаров."""
        return self.get("/api/v1/analytics/goods-labeling", params=params)

    def create_acceptance_report(self, payload: dict[str, Any]) -> Any:
        """Создать задачу отчёта приёмки."""
        return self.post("/api/v1/acceptance_report", json=payload)

    def get_acceptance_report_task_status(self, task_id: int) -> Any:
        """Статус задачи отчёта приёмки."""
        return self.get(f"/api/v1/acceptance_report/tasks/{task_id}/status")

    def get_acceptance_report_task_download(self, task_id: int) -> bytes:
        """Скачать отчёт приёмки."""
        return self._client.request_raw(
            "GET",
            f"{self._base_url}/api/v1/acceptance_report/tasks/{task_id}/download",
            domain="analytics",
        )

    def get_paid_storage(self, params: dict[str, Any]) -> Any:
        """Платное хранение."""
        return self.get("/api/v1/paid_storage", params=params)

    def get_paid_storage_task_status(self, task_id: int) -> Any:
        """Статус задачи платного хранения."""
        return self.get(f"/api/v1/paid_storage/tasks/{task_id}/status")

    def get_paid_storage_task_download(self, task_id: int) -> bytes:
        """Скачать отчёт платного хранения."""
        return self._client.request_raw(
            "GET",
            f"{self._base_url}/api/v1/paid_storage/tasks/{task_id}/download",
            domain="analytics",
        )

    def get_region_sale(self, params: dict[str, Any]) -> Any:
        """Продажи по регионам."""
        return self.get("/api/v1/analytics/region-sale", params=params)

    def get_brand_share_brands(self, params: dict[str, Any]) -> Any:
        """Бренды для доли бренда."""
        return self.get("/api/v1/analytics/brand-share/brands", params=params)

    def get_brand_share_parent_subjects(self, params: dict[str, Any]) -> Any:
        """Родительские предметы для доли бренда."""
        return self.get(
            "/api/v1/analytics/brand-share/parent-subjects",
            params=params,
        )

    def get_brand_share(self, params: dict[str, Any]) -> Any:
        """Доля бренда."""
        return self.get("/api/v1/analytics/brand-share", params=params)

    def get_banned_products_blocked(self, params: dict[str, Any]) -> Any:
        """Заблокированные товары."""
        return self.get("/api/v1/analytics/banned-products/blocked", params=params)

    def get_banned_products_shadowed(self, params: dict[str, Any]) -> Any:
        """Затенённые товары."""
        return self.get("/api/v1/analytics/banned-products/shadowed", params=params)

    def get_goods_return(self, params: dict[str, Any]) -> Any:
        """Возвраты товаров."""
        return self.get("/api/v1/analytics/goods-return", params=params)
