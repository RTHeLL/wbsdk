"""API баланса и финансов (finance-api, statistics, documents-api)."""

from typing import Any

from wbsdk.api.base import BaseAPI


class FinancesAPI(BaseAPI):
    """API баланса продавца (finance-api)."""

    def __init__(self, client: Any, base_url: str):
        super().__init__(client, base_url, domain="finance")

    def get_balance(self) -> Any:
        """Баланс продавца (текущий и доступный к выводу)."""
        return self.get("/api/v1/account/balance")


class DocumentsAPI(BaseAPI):
    """API документов продавца (documents-api)."""

    def __init__(self, client: Any, base_url: str):
        super().__init__(client, base_url, domain="documents")

    def get_categories(self, *, locale: str = "ru") -> Any:
        """Категории документов."""
        return self.get("/api/v1/documents/categories", params={"locale": locale})

    def get_documents_list(self, params: dict[str, Any]) -> Any:
        """Список документов."""
        return self.get("/api/v1/documents/list", params=params)

    def get_document_download(self, params: dict[str, Any]) -> Any:
        """Скачать один документ."""
        return self.get("/api/v1/documents/download", params=params)

    def get_documents_download_all(self, payload: dict[str, Any]) -> Any:
        """Скачать несколько документов (архив)."""
        return self.post("/api/v1/documents/download/all", json=payload)
