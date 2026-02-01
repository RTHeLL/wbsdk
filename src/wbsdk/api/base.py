"""Базовый класс для API-модулей."""

from typing import TYPE_CHECKING, Any

import httpx

from wbsdk.exceptions import (
    WBAPIError,
    WBConflictError,
    WBAuthError,
    WBNotFoundError,
    WBRateLimitError,
    WBValidationError,
)

if TYPE_CHECKING:
    from wbsdk.client import WBClient


class BaseAPI:
    """Базовый класс для всех API-модулей."""

    def __init__(self, client: "WBClient", base_url: str, domain: str = "marketplace"):
        self._client = client
        self._base_url = base_url.rstrip("/")
        self._domain = domain

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict | list | None = None,
        data: Any = None,
        files: dict | None = None,
        headers: dict[str, str] | None = None,
    ) -> Any:
        """Выполняет HTTP-запрос к API."""
        return self._client.request(
            method=method,
            url=f"{self._base_url}{path}",
            params=params,
            json=json,
            data=data,
            files=files,
            headers=headers,
            domain=self._domain,
        )

    def _raise_for_status(self, response: httpx.Response) -> None:
        """Преобразует HTTP-ошибки в исключения SDK."""
        if response.is_success:
            return

        try:
            data = response.json()
        except Exception:
            data = {"detail": response.text or str(response.status_code)}

        error_classes = {
            400: WBValidationError,
            401: WBAuthError,
            403: WBAuthError,
            404: WBNotFoundError,
            409: WBConflictError,
            422: WBValidationError,
            429: WBRateLimitError,
        }
        error_class = error_classes.get(response.status_code, WBAPIError)
        raise error_class(
            message=f"API request failed",
            status_code=response.status_code,
            response_data=data,
        )

    def get(self, path: str, *, params: dict[str, Any] | None = None, **kwargs: Any) -> Any:
        """GET-запрос."""
        return self._request("GET", path, params=params, **kwargs)

    def post(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict | list | None = None,
        data: Any = None,
        files: dict | None = None,
        **kwargs: Any,
    ) -> Any:
        """POST-запрос."""
        return self._request("POST", path, params=params, json=json, data=data, files=files, **kwargs)

    def put(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict | None = None,
        **kwargs: Any,
    ) -> Any:
        """PUT-запрос."""
        return self._request("PUT", path, params=params, json=json, **kwargs)

    def patch(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict | None = None,
        **kwargs: Any,
    ) -> Any:
        """PATCH-запрос."""
        return self._request("PATCH", path, params=params, json=json, **kwargs)

    def delete(self, path: str, *, params: dict[str, Any] | None = None, **kwargs: Any) -> Any:
        """DELETE-запрос."""
        return self._request("DELETE", path, params=params, **kwargs)
