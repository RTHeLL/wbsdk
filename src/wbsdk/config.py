"""Константы и базовые URL для WB API."""

# Базовые URL доменов WB API
BASE_URLS = {
    "content": "https://content-api.wildberries.ru",
    "marketplace": "https://marketplace-api.wildberries.ru",
    "prices": "https://discounts-prices-api.wildberries.ru",
    "analytics": "https://seller-analytics-api.wildberries.ru",
    "advert": "https://advert-api.wildberries.ru",
    "advert_media": "https://advert-media-api.wildberries.ru",
    "dp_calendar": "https://dp-calendar-api.wildberries.ru",
    "feedbacks": "https://feedbacks-api.wildberries.ru",
    "buyer_chat": "https://buyer-chat-api.wildberries.ru",
    "returns": "https://returns-api.wildberries.ru",
    "common": "https://common-api.wildberries.ru",
    "user_management": "https://user-management-api.wildberries.ru",
    "supplies": "https://supplies-api.wildberries.ru",
    "statistics": "https://statistics-api.wildberries.ru",
    "finance": "https://finance-api.wildberries.ru",
    "documents": "https://documents-api.wildberries.ru",
    "wbd": "https://devapi-digital.wildberries.ru",
}

# Базовые URL песочницы WB API (https://dev.wildberries.ru/sandbox)
SANDBOX_BASE_URLS = {
    "content": "https://content-api-sandbox.wildberries.ru",
    "marketplace": "https://marketplace-api-sandbox.wildberries.ru",
    "prices": "https://discounts-prices-api-sandbox.wildberries.ru",
    "analytics": "https://statistics-api-sandbox.wildberries.ru",
    "advert": "https://advert-api-sandbox.wildberries.ru",
    "feedbacks": "https://feedbacks-api-sandbox.wildberries.ru",
}

# Rate limits по доменам: (requests_per_period, period_seconds, min_interval_ms)
RATE_LIMITS = {
    "content": (100, 60, 600),
    "marketplace": (300, 60, 200),
    "prices": (10, 6, 600),
    "analytics": (3, 60, 20000),
    "advert": (5, 1, 200),
    "advert_media": (10, 1, 100),
    "dp_calendar": (10, 6, 600),
    "feedbacks": (3, 1, 333),
    "buyer_chat": (10, 10, 1000),
    "returns": (20, 60, 3000),
    "common": (60, 60, 1000),
    "user_management": (5, 1, 200),
    "supplies": (300, 60, 200),
    "statistics": (300, 60, 200),
    "finance": (1, 60, 60000),
    "documents": (5, 10, 2000),
    "wbd": (60, 60, 1000),
}

DEFAULT_TIMEOUT = 30.0
DEFAULT_RETRY_ATTEMPTS = 3
DEFAULT_RETRY_BACKOFF = 1.0
