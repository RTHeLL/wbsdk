"""Протоколы для типизации клиентов WB API (sync/async)."""

from typing import Any, Protocol


class RequestClientProtocol(Protocol):
    """Контракт для клиента WB API: методы request и request_raw."""

    def request(
        self,
        method: str,
        url: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict | list | None = None,
        data: Any = None,
        files: dict | None = None,
        headers: dict[str, str] | None = None,
        domain: str = "marketplace",
    ) -> Any:
        """Выполняет HTTP-запрос. Sync-клиент возвращает результат, async — корутину."""
        ...

    def request_raw(
        self,
        method: str,
        url: str,
        *,
        params: dict[str, Any] | None = None,
        domain: str = "marketplace",
    ) -> Any:
        """Выполняет запрос и возвращает сырые байты. Sync — bytes, async — корутину."""
        ...
