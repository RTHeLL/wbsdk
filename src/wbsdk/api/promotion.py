"""API рекламных кампаний (advert-api)."""

from typing import Any

from wbsdk.api.base import BaseAPI


class PromotionAPI(BaseAPI):
    """API продвижения: кампании, ставки, бюджет, статистика."""

    def __init__(self, client: Any, base_url: str):
        super().__init__(client, base_url, domain="advert")

    def get_promotion_count(self) -> Any:
        """Списки кампаний с ID (сгруппированы по типу и статусу)."""
        return self.get("/adv/v1/promotion/count")

    def get_adverts(self, params: dict[str, Any] | None = None) -> Any:
        """Информация о кампаниях."""
        return self.get("/api/advert/v2/adverts", params=params)

    def get_bids_min(self, params: dict[str, Any]) -> Any:
        """Минимальные ставки."""
        return self.get("/api/advert/v1/bids/min", params=params)

    def save_seacat_ad(self, payload: dict[str, Any]) -> Any:
        """Создать/обновить кампанию (seacat)."""
        return self.post("/adv/v2/seacat/save-ad", json=payload)

    def get_supplier_subjects(self) -> Any:
        """Предметы продавца для рекламы."""
        return self.get("/adv/v1/supplier/subjects")

    def get_supplier_nms(self, params: dict[str, Any]) -> Any:
        """Номенклатуры продавца."""
        return self.get("/adv/v2/supplier/nms", params=params)

    def delete_campaign(self, payload: dict[str, Any]) -> Any:
        """Удалить кампанию."""
        return self.post("/adv/v0/delete", json=payload)

    def rename_campaign(self, payload: dict[str, Any]) -> Any:
        """Переименовать кампанию."""
        return self.post("/adv/v0/rename", json=payload)

    def start_campaign(self, payload: dict[str, Any]) -> Any:
        """Запустить кампанию."""
        return self.post("/adv/v0/start", json=payload)

    def pause_campaign(self, payload: dict[str, Any]) -> Any:
        """Приостановить кампанию."""
        return self.post("/adv/v0/pause", json=payload)

    def stop_campaign(self, payload: dict[str, Any]) -> Any:
        """Остановить кампанию."""
        return self.post("/adv/v0/stop", json=payload)

    def get_auction_placements(self) -> Any:
        """Размещения аукциона."""
        return self.get("/adv/v0/auction/placements")

    def get_bids(self, params: dict[str, Any]) -> Any:
        """Ставки кампаний."""
        return self.get("/api/advert/v1/bids", params=params)

    def get_balance(self) -> Any:
        """Баланс рекламного счёта."""
        return self.get("/adv/v1/balance")

    def get_budget(self, payload: dict[str, Any]) -> Any:
        """Бюджет кампаний."""
        return self.post("/adv/v1/budget", json=payload)

    def budget_deposit(self, payload: dict[str, Any]) -> Any:
        """Пополнить бюджет кампании."""
        return self.post("/adv/v1/budget/deposit", json=payload)

    def upd_campaign(self, payload: dict[str, Any]) -> Any:
        """Обновить кампанию (upd)."""
        return self.post("/adv/v1/upd", json=payload)

    def get_payments(self, params: dict[str, Any]) -> Any:
        """Платежи по рекламе."""
        return self.get("/adv/v1/payments", params=params)

    def get_auction_nms(self, payload: dict[str, Any]) -> Any:
        """Аукцион по номенклатурам."""
        return self.post("/adv/v0/auction/nms", json=payload)

    def get_normquery_stats(self, payload: dict[str, Any]) -> Any:
        """Статистика по нормзапросам (v0)."""
        return self.post("/adv/v0/normquery/stats", json=payload)

    def get_normquery_bids(self, payload: dict[str, Any]) -> Any:
        """Получить ставки по нормзапросам."""
        return self.post("/adv/v0/normquery/get-bids", json=payload)

    def set_normquery_bids(self, payload: dict[str, Any]) -> Any:
        """Установить ставки по нормзапросам."""
        return self.post("/adv/v0/normquery/bids", json=payload)

    def get_normquery_minus(self, payload: dict[str, Any]) -> Any:
        """Минус-слова по нормзапросам."""
        return self.post("/adv/v0/normquery/get-minus", json=payload)

    def set_normquery_minus(self, payload: dict[str, Any]) -> Any:
        """Установить минус-слова."""
        return self.post("/adv/v0/normquery/set-minus", json=payload)

    def get_count(self, params: dict[str, Any]) -> Any:
        """Количество (adv/v1/count)."""
        return self.get("/adv/v1/count", params=params)

    def get_adverts_list(self, params: dict[str, Any]) -> Any:
        """Список кампаний (adv/v1/adverts)."""
        return self.get("/adv/v1/adverts", params=params)

    def get_advert(self, params: dict[str, Any]) -> Any:
        """Одна кампания по ID."""
        return self.get("/adv/v1/advert", params=params)

    def get_fullstats(self, payload: dict[str, Any]) -> Any:
        """Полная статистика (v3)."""
        return self.post("/adv/v3/fullstats", json=payload)

    def get_stats(self, params: dict[str, Any]) -> Any:
        """Статистика кампаний (v1)."""
        return self.get("/adv/v1/stats", params=params)

    def get_normquery_list(self, payload: dict[str, Any]) -> Any:
        """Список нормзапросов."""
        return self.post("/adv/v0/normquery/list", json=payload)

    def get_normquery_stats_v1(self, payload: dict[str, Any]) -> Any:
        """Статистика по нормзапросам (v1)."""
        return self.post("/adv/v1/normquery/stats", json=payload)


class PromotionCalendarAPI(BaseAPI):
    """API календаря акций (dp-calendar-api)."""

    def __init__(self, client: Any, base_url: str):
        super().__init__(client, base_url, domain="dp_calendar")

    def get_promotions(self, params: dict[str, Any]) -> Any:
        """Список акций."""
        return self.get("/api/v1/calendar/promotions", params=params)

    def get_promotions_details(self, params: dict[str, Any]) -> Any:
        """Детали акций."""
        return self.get("/api/v1/calendar/promotions/details", params=params)

    def get_promotions_nomenclatures(self, params: dict[str, Any]) -> Any:
        """Номенклатуры акций."""
        return self.get("/api/v1/calendar/promotions/nomenclatures", params=params)

    def upload_promotions(self, payload: dict[str, Any]) -> Any:
        """Загрузить акции."""
        return self.post("/api/v1/calendar/promotions/upload", json=payload)
