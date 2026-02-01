"""Базовый HTTP-клиент WB API."""

import time
from typing import Any

import httpx

from wbsdk.config import (
    BASE_URLS,
    DEFAULT_RETRY_ATTEMPTS,
    DEFAULT_RETRY_BACKOFF,
    DEFAULT_TIMEOUT,
    SANDBOX_BASE_URLS,
)
from wbsdk.exceptions import WBAPIError, raise_for_status
from wbsdk.rate_limiter import RateLimiter

# Импорты для избежания циклических зависимостей при инициализации API
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wbsdk.api.analytics import AnalyticsAPI
    from wbsdk.api.content import ContentAPI
    from wbsdk.api.marketplace import MarketplaceAPI
    from wbsdk.api.prices import PricesAPI
    from wbsdk.api.warehouses import WarehousesAPI


class WBClient:
    """Главный клиент Wildberries API.

    Для работы с песочницей WB (https://dev.wildberries.ru/sandbox) передайте
    sandbox=True. Токен должен быть с опцией «Тестовый контур» в личном кабинете WB.
    """

    def __init__(
        self,
        token: str,
        *,
        timeout: float = DEFAULT_TIMEOUT,
        retry_attempts: int = DEFAULT_RETRY_ATTEMPTS,
        retry_backoff: float = DEFAULT_RETRY_BACKOFF,
        base_urls: dict[str, str] | None = None,
        sandbox: bool = False,
    ):
        if not token or not isinstance(token, str):
            raise ValueError("Токен обязателен и должен быть непустой строкой")

        self._token = token
        self._timeout = timeout
        self._retry_attempts = retry_attempts
        self._retry_backoff = retry_backoff
        if base_urls is not None:
            self._base_urls = base_urls
        elif sandbox:
            self._base_urls = {**BASE_URLS, **SANDBOX_BASE_URLS}
        else:
            self._base_urls = BASE_URLS.copy()
        self._rate_limiter = RateLimiter()
        self._http_client = httpx.Client(
            timeout=timeout,
            headers={"Authorization": self._token},
        )

        # Ленивая инициализация API (избегаем циклических импортов)
        self._content: "ContentAPI | None" = None
        self._prices: "PricesAPI | None" = None
        self._marketplace: "MarketplaceAPI | None" = None
        self._warehouses: "WarehousesAPI | None" = None
        self._analytics: "AnalyticsAPI | None" = None

    def _wait_rate_limit(self, domain: str) -> None:
        """Ожидает соблюдения rate limit для домена."""
        self._rate_limiter.acquire(domain)

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
        """Выполняет HTTP-запрос с retry при 429."""
        self._wait_rate_limit(domain)

        request_headers = {"Authorization": self._token}
        if headers:
            request_headers.update(headers)

        last_error: Exception | None = None
        for attempt in range(self._retry_attempts):
            try:
                response = self._http_client.request(
                    method=method,
                    url=url,
                    params=params,
                    json=json,
                    data=data,
                    files=files,
                    headers=request_headers,
                )

                if response.status_code == 429:
                    retry_after = response.headers.get("Retry-After", "60")
                    wait_time = float(retry_after) if retry_after.isdigit() else 60.0
                    if attempt < self._retry_attempts - 1:
                        time.sleep(wait_time)
                        continue
                    from wbsdk.exceptions import WBRateLimitError
                    raise WBRateLimitError(
                        "Превышен лимит запросов",
                        status_code=429,
                        response_data=response.json() if response.content else {},
                    )

                if not response.is_success:
                    try:
                        error_data = response.json()
                    except Exception:
                        error_data = {}
                    raise_for_status(response.status_code, error_data, response.text)

                if response.status_code in (204, 205):
                    return None

                if response.content:
                    return response.json()
                return None

            except WBAPIError:
                raise
            except httpx.HTTPError as e:
                last_error = e
                if attempt < self._retry_attempts - 1:
                    time.sleep(self._retry_backoff * (2**attempt))
                else:
                    raise

        if last_error:
            raise last_error
        return None

    def request_raw(
        self,
        method: str,
        url: str,
        *,
        params: dict[str, Any] | None = None,
        domain: str = "marketplace",
    ) -> bytes:
        """Выполняет запрос и возвращает сырые байты (для скачивания файлов)."""
        self._wait_rate_limit(domain)
        response = self._http_client.request(
            method=method,
            url=url,
            params=params,
            headers={"Authorization": self._token},
        )
        if not response.is_success:
            try:
                error_data = response.json()
            except Exception:
                error_data = {}
            raise_for_status(response.status_code, error_data, response.text)
        return response.content

    def close(self) -> None:
        """Закрывает HTTP-клиент."""
        self._http_client.close()

    def __enter__(self) -> "WBClient":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    @property
    def content(self) -> "ContentAPI":
        """API контента и карточек товаров."""
        if self._content is None:
            from wbsdk.api.content import ContentAPI
            base_url = self._base_urls.get("content", BASE_URLS["content"])
            self._content = ContentAPI(self, base_url)
        return self._content

    @property
    def prices(self) -> "PricesAPI":
        """API цен и скидок."""
        if self._prices is None:
            from wbsdk.api.prices import PricesAPI
            base_url = self._base_urls.get("prices", BASE_URLS["prices"])
            self._prices = PricesAPI(self, base_url)
        return self._prices

    @property
    def marketplace(self) -> "MarketplaceAPI":
        """API заказов FBS и поставок."""
        if self._marketplace is None:
            from wbsdk.api.marketplace import MarketplaceAPI
            base_url = self._base_urls.get("marketplace", BASE_URLS["marketplace"])
            self._marketplace = MarketplaceAPI(self, base_url)
        return self._marketplace

    @property
    def warehouses(self) -> "WarehousesAPI":
        """API складов продавца (DBW)."""
        if self._warehouses is None:
            from wbsdk.api.warehouses import WarehousesAPI
            base_url = self._base_urls.get("marketplace", BASE_URLS["marketplace"])
            self._warehouses = WarehousesAPI(self, base_url)
        return self._warehouses

    @property
    def analytics(self) -> "AnalyticsAPI":
        """API аналитики."""
        if self._analytics is None:
            from wbsdk.api.analytics import AnalyticsAPI
            base_url = self._base_urls.get("analytics", BASE_URLS["analytics"])
            self._analytics = AnalyticsAPI(self, base_url)
        return self._analytics
