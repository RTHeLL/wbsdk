"""Базовый класс для API-модулей."""

import inspect
from typing import Any, get_args, get_origin

import httpx
from pydantic import TypeAdapter

from wbsdk._protocols import RequestClientProtocol
from wbsdk.exceptions import (
    WBAPIError,
    WBConflictError,
    WBAuthError,
    WBNotFoundError,
    WBRateLimitError,
    WBValidationError,
)


class BaseAPI:
    """Базовый класс для всех API-модулей."""

    def __init__(
        self,
        client: RequestClientProtocol,
        base_url: str,
        domain: str = "marketplace",
    ):
        self._client = client
        self._base_url = base_url.rstrip("/")
        self._domain = domain

    def _parse_response(self, result: Any, response_model: type) -> Any:
        """Парсит ответ через Pydantic-модель или TypeAdapter для list."""
        if result is None:
            return None
        origin = get_origin(response_model)
        if origin is list:
            item_model = get_args(response_model)[0]
            adapter = TypeAdapter(list[item_model])
            return adapter.validate_python(result)
        return response_model.model_validate(result)

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
        response_model: type | None = None,
    ) -> Any:
        """Выполняет HTTP-запрос к API. При async-клиенте возвращает корутину."""
        result = self._client.request(
            method=method,
            url=f"{self._base_url}{path}",
            params=params,
            json=json,
            data=data,
            files=files,
            headers=headers,
            domain=self._domain,
        )
        if inspect.iscoroutine(result):
            # AsyncWBClient: оборачиваем в корутину с парсингом после await
            async def _await_and_parse() -> Any:
                raw = await result
                if response_model is not None and raw is not None:
                    return self._parse_response(raw, response_model)
                return raw

            return _await_and_parse()
        if response_model is not None and result is not None:
            return self._parse_response(result, response_model)
        return result

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

    def get(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        response_model: type | None = None,
        **kwargs: Any,
    ) -> Any:
        """GET-запрос."""
        return self._request("GET", path, params=params, response_model=response_model, **kwargs)

    def post(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict | list | None = None,
        data: Any = None,
        files: dict | None = None,
        response_model: type | None = None,
        **kwargs: Any,
    ) -> Any:
        """POST-запрос."""
        return self._request(
            "POST",
            path,
            params=params,
            json=json,
            data=data,
            files=files,
            response_model=response_model,
            **kwargs,
        )

    def put(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict | None = None,
        response_model: type | None = None,
        **kwargs: Any,
    ) -> Any:
        """PUT-запрос."""
        return self._request(
            "PUT", path, params=params, json=json, response_model=response_model, **kwargs
        )

    def patch(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict | None = None,
        response_model: type | None = None,
        **kwargs: Any,
    ) -> Any:
        """PATCH-запрос."""
        return self._request(
            "PATCH", path, params=params, json=json, response_model=response_model, **kwargs
        )

    def delete(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        response_model: type | None = None,
        **kwargs: Any,
    ) -> Any:
        """DELETE-запрос."""
        return self._request(
            "DELETE", path, params=params, response_model=response_model, **kwargs
        )
