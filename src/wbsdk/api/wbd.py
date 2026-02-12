"""API цифровых товаров WBD (devapi-digital)."""

from typing import Any

from wbsdk.api.base import BaseAPI


class WBDAPI(BaseAPI):
    """API ключей, офферов и контента WBD (цифровые товары)."""

    def __init__(self, client: Any, base_url: str):
        super().__init__(client, base_url, domain="wbd")

    # --- Ключи API ---

    def get_keys(self, params: dict[str, Any] | None = None) -> Any:
        """Список ключей API."""
        return self.get("/api/v1/keys-api/keys", params=params)

    def get_keys_redeemed(self, params: dict[str, Any] | None = None) -> Any:
        """Погашенные ключи."""
        return self.get("/api/v1/keys-api/keys/redeemed", params=params)

    # --- Офферы ---

    def get_offer_keys(self, offer_id: int, params: dict[str, Any] | None = None) -> Any:
        """Ключи оффера."""
        return self.get(f"/api/v1/offer/keys/{offer_id}", params=params)

    def get_offer_keys_list(self, offer_id: int, payload: dict[str, Any]) -> Any:
        """Список ключей оффера."""
        return self.post(f"/api/v1/offer/keys/{offer_id}/list", json=payload)

    def get_offers(self, params: dict[str, Any] | None = None) -> Any:
        """Список офферов."""
        return self.get("/api/v1/offers", params=params)

    def get_offers_thumb(self, payload: dict[str, Any]) -> Any:
        """Превью офферов."""
        return self.post("/api/v1/offers/thumb", json=payload)

    def get_offer(self, offer_id: int) -> Any:
        """Один оффер по ID."""
        return self.get(f"/api/v1/offers/{offer_id}")

    def get_offers_author(self, params: dict[str, Any] | None = None) -> Any:
        """Офферы по автору."""
        return self.get("/api/v1/offers/author", params=params)

    def get_offer_price(self, offer_id: int) -> Any:
        """Цена оффера."""
        return self.get(f"/api/v1/offer/price/{offer_id}")

    def get_offer_detail(self, offer_id: int) -> Any:
        """Детали оффера (offer/{id})."""
        return self.get(f"/api/v1/offer/{offer_id}")

    def get_catalog(self, params: dict[str, Any] | None = None) -> Any:
        """Каталог."""
        return self.get("/api/v1/catalog", params=params)

    # --- Контент ---

    def get_content_illustration(self, params: dict[str, Any]) -> Any:
        """Иллюстрация контента."""
        return self.get("/api/v1/content/illustration", params=params)

    def content_upload_init(self, payload: dict[str, Any]) -> Any:
        """Инициализация загрузки контента."""
        return self.post("/api/v1/content/upload/init", json=payload)

    def content_upload_chunk(self, payload: dict[str, Any]) -> Any:
        """Загрузка чанка контента."""
        return self.post("/api/v1/content/upload/chunk", json=payload)

    def get_content_author(self, content_id: int | None = None) -> Any:
        """Автор контента (один или список)."""
        if content_id is not None:
            return self.get(f"/api/v1/content/author/{content_id}")
        return self.get("/api/v1/content/author")

    def content_author_create_or_update(self, payload: dict[str, Any]) -> Any:
        """Создать/обновить автора контента."""
        return self.post("/api/v1/content/author", json=payload)

    def get_content_download(self, uri: str) -> Any:
        """Скачать контент по URI."""
        return self.get(f"/api/v1/content/download/{uri}")

    def content_delete(self, payload: dict[str, Any]) -> Any:
        """Удалить контент."""
        return self.post("/api/v1/content/delete", json=payload)

    def get_content_gallery(self, params: dict[str, Any]) -> Any:
        """Галерея контента."""
        return self.get("/api/v1/content/gallery", params=params)
