"""Асинхронный HTTP-клиент WB API."""

import asyncio
import logging
from typing import TYPE_CHECKING, Any

import httpx

from wbsdk.client import logger
from wbsdk.config import (
    BASE_URLS,
    DEFAULT_RETRY_ATTEMPTS,
    DEFAULT_RETRY_BACKOFF,
    DEFAULT_TIMEOUT,
    SANDBOX_BASE_URLS,
)
from wbsdk.exceptions import WBAPIError, raise_for_status
from wbsdk.rate_limiter import AsyncRateLimiter

if TYPE_CHECKING:
    from wbsdk.api.analytics import AnalyticsAPI
    from wbsdk.api.click_collect import ClickCollectAPI
    from wbsdk.api.communications import CommunicationsAPI
    from wbsdk.api.content import ContentAPI
    from wbsdk.api.finances import DocumentsAPI, FinancesAPI
    from wbsdk.api.general import GeneralAPI
    from wbsdk.api.marketplace import MarketplaceAPI
    from wbsdk.api.orders_dbs import OrdersDBSAPI
    from wbsdk.api.orders_dbw import OrdersDBWAPI
    from wbsdk.api.orders_fbw import OrdersFBWAPI
    from wbsdk.api.prices import PricesAPI
    from wbsdk.api.promotion import PromotionAPI, PromotionCalendarAPI
    from wbsdk.api.reports import ReportsAPI
    from wbsdk.api.tariffs import TariffsAPI
    from wbsdk.api.user_management import UserManagementAPI
    from wbsdk.api.warehouses import WarehousesAPI
    from wbsdk.api.wbd import WBDAPI


class AsyncWBClient:
    """Асинхронный клиент Wildberries API.

    Используйте "async with AsyncWBClient(token) as client:" или явно
    "await client.close()" после работы, чтобы корректно закрыть соединения.

    При debug=True (или при уровне DEBUG логгера ``wbsdk``) в лог выводятся метод,
    URL, домен и код/размер ответа; токен и тела запросов/ответов не логируются.
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
        debug: bool = False,
    ):
        if not token or not isinstance(token, str):
            raise ValueError("Токен обязателен и должен быть непустой строкой")

        self._token = token
        self._timeout = timeout
        self._retry_attempts = retry_attempts
        self._retry_backoff = retry_backoff
        self._debug = debug
        if base_urls is not None:
            self._base_urls = base_urls
        elif sandbox:
            self._base_urls = {**BASE_URLS, **SANDBOX_BASE_URLS}
        else:
            self._base_urls = BASE_URLS.copy()
        self._rate_limiter = AsyncRateLimiter()
        self._http_client = httpx.AsyncClient(
            timeout=timeout,
            headers={"Authorization": self._token},
        )

        self._content: ContentAPI | None = None
        self._prices: PricesAPI | None = None
        self._marketplace: MarketplaceAPI | None = None
        self._warehouses: WarehousesAPI | None = None
        self._analytics: AnalyticsAPI | None = None
        self._general: GeneralAPI | None = None
        self._user_management: UserManagementAPI | None = None
        self._tariffs: TariffsAPI | None = None
        self._orders_dbw: OrdersDBWAPI | None = None
        self._orders_dbs: OrdersDBSAPI | None = None
        self._click_collect: ClickCollectAPI | None = None
        self._orders_fbw: OrdersFBWAPI | None = None
        self._communications: CommunicationsAPI | None = None
        self._reports: ReportsAPI | None = None
        self._promotion: PromotionAPI | None = None
        self._promotion_calendar: PromotionCalendarAPI | None = None
        self._finances: FinancesAPI | None = None
        self._documents: DocumentsAPI | None = None
        self._wbd: WBDAPI | None = None

    async def _wait_rate_limit(self, domain: str) -> None:
        """Ожидает соблюдения rate limit для домена."""
        await self._rate_limiter.acquire(domain)

    def _should_log(self) -> bool:
        """Проверяет, нужно ли логировать запросы (debug или уровень DEBUG)."""
        return self._debug or logger.isEnabledFor(logging.DEBUG)

    def _log_response(self, method: str, url: str, response: httpx.Response) -> None:
        """Логирует ответ (метод, URL, код, размер)."""
        size = response.headers.get("Content-Length")
        if size is None and response.content is not None:
            size = str(len(response.content))
        size_str = size if size is not None else "?"
        logger.debug(
            "WB API response: %s %s -> %d (%s bytes)",
            method,
            url,
            response.status_code,
            size_str,
        )

    async def request(
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
        await self._wait_rate_limit(domain)
        if self._should_log():
            logger.debug("WB API request: %s %s [domain=%s]", method, url, domain)

        request_headers = {"Authorization": self._token}
        if headers:
            request_headers.update(headers)

        last_error: Exception | None = None
        for attempt in range(self._retry_attempts):
            try:
                response = await self._http_client.request(
                    method=method,
                    url=url,
                    params=params,
                    json=json,
                    data=data,
                    files=files,
                    headers=request_headers,
                )
                if self._should_log():
                    self._log_response(method, url, response)

                if response.status_code == 429:
                    retry_after = response.headers.get("Retry-After", "60")
                    wait_time = float(retry_after) if retry_after.isdigit() else 60.0
                    if attempt < self._retry_attempts - 1:
                        await asyncio.sleep(wait_time)
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
                    await asyncio.sleep(self._retry_backoff * (2**attempt))
                else:
                    raise

        if last_error:
            raise last_error
        return None

    async def request_raw(
        self,
        method: str,
        url: str,
        *,
        params: dict[str, Any] | None = None,
        domain: str = "marketplace",
    ) -> bytes:
        """Выполняет запрос и возвращает сырые байты (для скачивания файлов)."""
        await self._wait_rate_limit(domain)
        if self._should_log():
            logger.debug("WB API request: %s %s [domain=%s]", method, url, domain)
        response = await self._http_client.request(
            method=method,
            url=url,
            params=params,
            headers={"Authorization": self._token},
        )
        if self._should_log():
            self._log_response(method, url, response)
        if not response.is_success:
            try:
                error_data = response.json()
            except Exception:
                error_data = {}
            raise_for_status(response.status_code, error_data, response.text)
        return response.content

    async def close(self) -> None:
        """Закрывает HTTP-клиент."""
        await self._http_client.aclose()

    async def __aenter__(self) -> "AsyncWBClient":
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()

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

    @property
    def general(self) -> "GeneralAPI":
        """API общего раздела: ping, новости, информация о продавце."""
        if self._general is None:
            from wbsdk.api.general import GeneralAPI

            base_url = self._base_urls.get("common", BASE_URLS["common"])
            self._general = GeneralAPI(self, base_url)
        return self._general

    @property
    def user_management(self) -> "UserManagementAPI":
        """API управления пользователями продавца."""
        if self._user_management is None:
            from wbsdk.api.user_management import UserManagementAPI

            base_url = self._base_urls.get("user_management", BASE_URLS["user_management"])
            self._user_management = UserManagementAPI(self, base_url)
        return self._user_management

    @property
    def tariffs(self) -> "TariffsAPI":
        """API тарифов и комиссий."""
        if self._tariffs is None:
            from wbsdk.api.tariffs import TariffsAPI

            base_url = self._base_urls.get("common", BASE_URLS["common"])
            self._tariffs = TariffsAPI(self, base_url)
        return self._tariffs

    @property
    def orders_dbw(self) -> "OrdersDBWAPI":
        """API заказов DBW (доставка курьером WB)."""
        if self._orders_dbw is None:
            from wbsdk.api.orders_dbw import OrdersDBWAPI

            base_url = self._base_urls.get("marketplace", BASE_URLS["marketplace"])
            self._orders_dbw = OrdersDBWAPI(self, base_url)
        return self._orders_dbw

    @property
    def orders_dbs(self) -> "OrdersDBSAPI":
        """API заказов DBS (витрина)."""
        if self._orders_dbs is None:
            from wbsdk.api.orders_dbs import OrdersDBSAPI

            base_url = self._base_urls.get("marketplace", BASE_URLS["marketplace"])
            self._orders_dbs = OrdersDBSAPI(self, base_url)
        return self._orders_dbs

    @property
    def click_collect(self) -> "ClickCollectAPI":
        """API заказов самовывоза (Click&Collect)."""
        if self._click_collect is None:
            from wbsdk.api.click_collect import ClickCollectAPI

            base_url = self._base_urls.get("marketplace", BASE_URLS["marketplace"])
            self._click_collect = ClickCollectAPI(self, base_url)
        return self._click_collect

    @property
    def orders_fbw(self) -> "OrdersFBWAPI":
        """API поставок FBW (склад WB)."""
        if self._orders_fbw is None:
            from wbsdk.api.orders_fbw import OrdersFBWAPI

            base_url = self._base_urls.get("supplies", BASE_URLS["supplies"])
            self._orders_fbw = OrdersFBWAPI(self, base_url)
        return self._orders_fbw

    @property
    def communications(self) -> "CommunicationsAPI":
        """API вопросов, отзывов, чатов и претензий."""
        if self._communications is None:
            from wbsdk.api.communications import CommunicationsAPI

            base_url = self._base_urls.get("feedbacks", BASE_URLS["feedbacks"])
            self._communications = CommunicationsAPI(self, base_url)
        return self._communications

    @property
    def reports(self) -> "ReportsAPI":
        """API отчётов: поставки, остатки, заказы, продажи."""
        if self._reports is None:
            from wbsdk.api.reports import ReportsAPI

            base_url = self._base_urls.get("statistics", BASE_URLS["statistics"])
            self._reports = ReportsAPI(self, base_url)
        return self._reports

    @property
    def promotion(self) -> "PromotionAPI":
        """API рекламных кампаний."""
        if self._promotion is None:
            from wbsdk.api.promotion import PromotionAPI

            base_url = self._base_urls.get("advert", BASE_URLS["advert"])
            self._promotion = PromotionAPI(self, base_url)
        return self._promotion

    @property
    def promotion_calendar(self) -> "PromotionCalendarAPI":
        """API календаря акций."""
        if self._promotion_calendar is None:
            from wbsdk.api.promotion import PromotionCalendarAPI

            base_url = self._base_urls.get("dp_calendar", BASE_URLS["dp_calendar"])
            self._promotion_calendar = PromotionCalendarAPI(self, base_url)
        return self._promotion_calendar

    @property
    def finances(self) -> "FinancesAPI":
        """API баланса продавца."""
        if self._finances is None:
            from wbsdk.api.finances import FinancesAPI

            base_url = self._base_urls.get("finance", BASE_URLS["finance"])
            self._finances = FinancesAPI(self, base_url)
        return self._finances

    @property
    def documents(self) -> "DocumentsAPI":
        """API документов продавца."""
        if self._documents is None:
            from wbsdk.api.finances import DocumentsAPI

            base_url = self._base_urls.get("documents", BASE_URLS["documents"])
            self._documents = DocumentsAPI(self, base_url)
        return self._documents

    @property
    def wbd(self) -> "WBDAPI":
        """API цифровых товаров WBD."""
        if self._wbd is None:
            from wbsdk.api.wbd import WBDAPI

            base_url = self._base_urls.get("wbd", BASE_URLS["wbd"])
            self._wbd = WBDAPI(self, base_url)
        return self._wbd
