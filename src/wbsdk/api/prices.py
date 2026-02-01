"""API цен и скидок."""

from typing import Any

from wbsdk.api.base import BaseAPI
from wbsdk.schemas.prices import (
    GoodsSizesResponse,
    GoodsWithPricesResponse,
    PriceUploadResponse,
    QuarantineGoodsResponse,
    UploadDetailsResponse,
    UploadStateResponse,
)


class PricesAPI(BaseAPI):
    """API для работы с ценами и скидками."""

    def __init__(self, client: Any, base_url: str):
        super().__init__(client, base_url, domain="prices")

    def set_prices(self, data: list[dict]) -> PriceUploadResponse:
        """Установка цен и скидок. Максимум 1000 товаров в запросе."""
        return self.post(
            "/api/v2/upload/task",
            json={"data": data},
            response_model=PriceUploadResponse,
        )

    def set_size_prices(self, data: list[dict]) -> PriceUploadResponse:
        """Установка цен по размерам (для товаров с editableSizePrice)."""
        return self.post(
            "/api/v2/upload/task/size",
            json={"data": data},
            response_model=PriceUploadResponse,
        )

    def set_club_discounts(self, data: list[dict]) -> PriceUploadResponse:
        """Установка скидок WB Клуба."""
        return self.post(
            "/api/v2/upload/task/club-discount",
            json={"data": data},
            response_model=PriceUploadResponse,
        )

    def get_processed_upload_state(self, upload_id: int) -> UploadStateResponse:
        """Статус обработанной выгрузки цен."""
        return self.get(
            "/api/v2/history/tasks",
            params={"uploadID": upload_id},
            response_model=UploadStateResponse,
        )

    def get_processed_upload_details(
        self,
        upload_id: int,
        *,
        limit: int = 1000,
        offset: int = 0,
    ) -> UploadDetailsResponse:
        """Детали обработанной выгрузки цен."""
        return self.get(
            "/api/v2/history/goods/task",
            params={"uploadID": upload_id, "limit": limit, "offset": offset},
            response_model=UploadDetailsResponse,
        )

    def get_unprocessed_upload_state(self, upload_id: int) -> UploadStateResponse:
        """Статус необработанной выгрузки."""
        return self.get(
            "/api/v2/buffer/tasks",
            params={"uploadID": upload_id},
            response_model=UploadStateResponse,
        )

    def get_unprocessed_upload_details(
        self,
        upload_id: int,
        *,
        limit: int = 1000,
        offset: int = 0,
    ) -> UploadDetailsResponse:
        """Детали необработанной выгрузки."""
        return self.get(
            "/api/v2/buffer/goods/task",
            params={"uploadID": upload_id, "limit": limit, "offset": offset},
            response_model=UploadDetailsResponse,
        )

    def get_goods_with_prices(
        self,
        *,
        limit: int = 1000,
        offset: int = 0,
        filter_nm_id: int | None = None,
    ) -> GoodsWithPricesResponse:
        """Список товаров с ценами."""
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if filter_nm_id is not None:
            params["filterNmID"] = filter_nm_id
        return self.get(
            "/api/v2/list/goods/filter",
            params=params,
            response_model=GoodsWithPricesResponse,
        )

    def get_goods_with_prices_by_articles(
        self, nm_list: list[int]
    ) -> GoodsWithPricesResponse:
        """Товары с ценами по артикулам (до 1000)."""
        return self.post(
            "/api/v2/list/goods/filter",
            json={"nmList": nm_list},
            response_model=GoodsWithPricesResponse,
        )

    def get_goods_sizes_with_prices(
        self,
        nm_id: int,
        *,
        limit: int = 1000,
        offset: int = 0,
    ) -> GoodsSizesResponse:
        """Цены по размерам товара."""
        return self.get(
            "/api/v2/list/goods/size/nm",
            params={"nmID": nm_id, "limit": limit, "offset": offset},
            response_model=GoodsSizesResponse,
        )

    def get_quarantine_goods(
        self,
        *,
        limit: int = 1000,
        offset: int = 0,
    ) -> QuarantineGoodsResponse:
        """Товары в карантине цен."""
        return self.get(
            "/api/v2/quarantine/goods",
            params={"limit": limit, "offset": offset},
            response_model=QuarantineGoodsResponse,
        )
