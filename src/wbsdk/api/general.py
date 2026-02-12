"""API общего раздела: ping, новости, информация о продавце (common-api)."""

from typing import Any

from wbsdk.api.base import BaseAPI
from wbsdk.schemas.general import (
    NewsResponse,
    PingResponse,
    SellerInfoResponse,
)


class GeneralAPI(BaseAPI):
    """API проверки подключения, новостей и информации о продавце."""

    def __init__(self, client: Any, base_url: str):
        super().__init__(client, base_url, domain="common")

    def ping(self) -> PingResponse:
        """Проверка подключения к WB API и валидности токена."""
        return self.get("/ping", response_model=PingResponse)

    def get_news(
        self,
        *,
        from_date: str | None = None,
        from_id: int | None = None,
    ) -> NewsResponse:
        """Новости портала продавцов. Нужен один из параметров: from_date или from_id."""
        params: dict[str, Any] = {}
        if from_date is not None:
            params["from"] = from_date
        if from_id is not None:
            params["fromID"] = from_id
        return self.get(
            "/api/communications/v2/news",
            params=params or None,
            response_model=NewsResponse,
        )

    def get_seller_info(self) -> SellerInfoResponse:
        """Информация о продавце: наименование и ID профиля."""
        return self.get(
            "/api/v1/seller-info",
            response_model=SellerInfoResponse,
        )
