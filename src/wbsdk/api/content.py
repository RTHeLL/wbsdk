"""API контента, карточек товаров, тегов и медиа."""

from pathlib import Path
from typing import Any

from wbsdk.api.base import BaseAPI


class ContentAPI(BaseAPI):
    """API для работы с контентом и карточками товаров."""

    def __init__(self, client: Any, base_url: str):
        super().__init__(client, base_url, domain="content")

    # --- Категории и справочники ---

    def get_parent_categories(self, *, locale: str | None = None) -> Any:
        """Возвращает список родительских категорий товаров."""
        params = {}
        if locale:
            params["locale"] = locale
        return self.get("/content/v2/object/parent/all", params=params or None)

    def get_subjects(
        self,
        *,
        locale: str | None = None,
        name: str | None = None,
        limit: int = 30,
        offset: int = 0,
        parent_id: int | None = None,
    ) -> Any:
        """Возвращает список предметов (подкатегорий)."""
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if locale:
            params["locale"] = locale
        if name:
            params["name"] = name
        if parent_id is not None:
            params["parentID"] = parent_id
        return self.get("/content/v2/object/all", params=params)

    def get_subject_characteristics(self, subject_id: int, *, locale: str | None = None) -> Any:
        """Возвращает характеристики предмета по ID."""
        params = {}
        if locale:
            params["locale"] = locale
        return self.get(f"/content/v2/object/charcs/{subject_id}", params=params or None)

    def get_colors(self, *, locale: str | None = None) -> Any:
        """Справочник цветов."""
        params = {}
        if locale:
            params["locale"] = locale
        return self.get("/content/v2/directory/colors", params=params or None)

    def get_genders(self, *, locale: str | None = None) -> Any:
        """Справочник пола."""
        params = {}
        if locale:
            params["locale"] = locale
        return self.get("/content/v2/directory/kinds", params=params or None)

    def get_countries(self, *, locale: str | None = None) -> Any:
        """Справочник стран производства."""
        params = {}
        if locale:
            params["locale"] = locale
        return self.get("/content/v2/directory/countries", params=params or None)

    def get_seasons(self, *, locale: str | None = None) -> Any:
        """Справочник сезонов."""
        params = {}
        if locale:
            params["locale"] = locale
        return self.get("/content/v2/directory/seasons", params=params or None)

    def get_vat_rates(self, *, locale: str | None = None) -> Any:
        """Справочник ставок НДС."""
        params = {}
        if locale:
            params["locale"] = locale
        return self.get("/content/v2/directory/vat", params=params or None)

    def get_tnved(
        self,
        subject_id: int,
        *,
        search: int | None = None,
        locale: str | None = None,
    ) -> Any:
        """Коды ТН ВЭД."""
        params: dict[str, Any] = {"subjectID": subject_id}
        if search is not None:
            params["search"] = search
        if locale:
            params["locale"] = locale
        return self.get("/content/v2/directory/tnved", params=params)

    def get_brands(self, subject_id: int, *, next_cursor: int | None = None) -> Any:
        """Список брендов по ID предмета."""
        params: dict[str, Any] = {"subjectId": subject_id}
        if next_cursor is not None:
            params["next"] = next_cursor
        return self.get("/api/content/v1/brands", params=params)

    # --- Карточки товаров ---

    def get_cards_limits(self) -> Any:
        """Лимиты на создание карточек."""
        return self.get("/content/v2/cards/limits")

    def generate_barcodes(self, count: int) -> Any:
        """Генерация штрихкодов (SKU)."""
        return self.post("/content/v2/barcodes", json={"count": count})

    def create_cards(self, cards: list[dict]) -> Any:
        """Создание карточек товаров."""
        return self.post("/content/v2/cards/upload", json=cards)

    def create_cards_with_merge(self, imt_id: int | None, cards_to_add: list[dict]) -> Any:
        """Создание карточек с объединением."""
        payload: dict[str, Any] = {"cardsToAdd": cards_to_add}
        if imt_id is not None:
            payload["imtID"] = imt_id
        return self.post("/content/v2/cards/upload/add", json=payload)

    def get_cards_list(
        self,
        settings: dict,
        *,
        locale: str | None = None,
    ) -> Any:
        """Список карточек товаров."""
        params = {}
        if locale:
            params["locale"] = locale
        return self.post(
            "/content/v2/get/cards/list",
            params=params or None,
            json={"settings": settings},
        )

    def get_cards_error_list(
        self,
        cursor: dict,
        *,
        order: dict | None = None,
        locale: str | None = None,
    ) -> Any:
        """Список карточек с ошибками."""
        params = {}
        if locale:
            params["locale"] = locale
        payload: dict[str, Any] = {"cursor": cursor}
        if order:
            payload["order"] = order
        return self.post(
            "/content/v2/cards/error/list",
            params=params or None,
            json=payload,
        )

    def update_cards(self, cards: list[dict]) -> Any:
        """Обновление карточек товаров."""
        return self.post("/content/v2/cards/update", json=cards)

    def move_cards(self, target_imt: int | None, nm_ids: list[int]) -> Any:
        """Объединение или разделение карточек."""
        if target_imt is not None:
            return self.post("/content/v2/cards/moveNm", json={"targetIMT": target_imt, "nmIDs": nm_ids})
        return self.post("/content/v2/cards/moveNm", json={"nmIDs": nm_ids})

    def move_cards_to_trash(self, nm_ids: list[int]) -> Any:
        """Перенос карточек в корзину."""
        return self.post("/content/v2/cards/delete/trash", json={"nmIDs": nm_ids})

    def recover_cards_from_trash(self, nm_ids: list[int]) -> Any:
        """Восстановление карточек из корзины."""
        return self.post("/content/v2/cards/recover", json={"nmIDs": nm_ids})

    def get_cards_trash_list(self, settings: dict, *, locale: str | None = None) -> Any:
        """Список карточек в корзине."""
        params = {}
        if locale:
            params["locale"] = locale
        return self.post(
            "/content/v2/get/cards/trash",
            params=params or None,
            json={"settings": settings},
        )

    # --- Медиа ---

    def upload_media_file(
        self,
        nm_id: int,
        photo_number: int,
        file_path: str | Path,
    ) -> Any:
        """Загрузка медиафайла для карточки."""
        path = Path(file_path)
        with open(path, "rb") as f:
            file_content = f.read()
        files = {"uploadfile": (path.name, file_content, "application/octet-stream")}
        return self.post(
            "/content/v3/media/file",
            files=files,
            headers={
                "X-Nm-Id": str(nm_id),
                "X-Photo-Number": str(photo_number),
            },
        )

    def upload_media_by_links(self, nm_id: int, data: list[str]) -> Any:
        """Загрузка медиа по ссылкам."""
        return self.post("/content/v3/media/save", json={"nmId": nm_id, "data": data})

    # --- Теги ---

    def get_tags(self) -> Any:
        """Список тегов продавца."""
        return self.get("/content/v2/tags")

    def create_tag(self, name: str, color: str) -> Any:
        """Создание тега."""
        return self.post("/content/v2/tag", json={"name": name, "color": color})

    def update_tag(self, tag_id: int, name: str, color: str) -> Any:
        """Обновление тега."""
        return self.patch(f"/content/v2/tag/{tag_id}", json={"name": name, "color": color})

    def delete_tag(self, tag_id: int) -> Any:
        """Удаление тега."""
        return self.delete(f"/content/v2/tag/{tag_id}")

    def link_tags_to_card(self, nm_id: int, tags_ids: list[int]) -> Any:
        """Привязка тегов к карточке товара."""
        return self.post("/content/v2/tag/nomenclature/link", json={"nmID": nm_id, "tagsIDs": tags_ids})
