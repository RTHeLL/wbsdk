# WB SDK

Профессиональный Python SDK для Wildberries API.

## Установка

```bash
pip install wbsdk
```

Или из исходников:

```bash
pip install -e .
```

## Быстрый старт

```python
from wbsdk import WBClient

client = WBClient(token="YOUR_API_TOKEN")

# Контент и карточки
categories = client.content.get_parent_categories()
cards = client.content.get_cards_list(settings={
    "cursor": {"limit": 100},
    "sort": {"ascending": True},
})

# Цены
client.prices.set_prices([{"nmID": 123, "price": 999, "discount": 30}])

# Заказы FBS
new_orders = client.marketplace.get_new_orders()
client.marketplace.create_supply(name="Поставка 1")

# Склады и остатки
warehouses = client.warehouses.get_warehouses()

# Аналитика
funnel = client.analytics.get_sales_funnel_products(
    selected_period={"start": "2024-01-01", "end": "2024-01-31"},
)
```

## Поддерживаемые API

- **Content** — карточки товаров, категории, теги, медиа
- **Prices** — цены, скидки, карантин
- **Marketplace (FBS)** — заказы, поставки, пропуска, метаданные
- **Warehouses** — склады продавца, остатки DBW
- **Analytics** — воронка продаж, поисковые запросы, отчёты по остаткам

## Обработка ошибок

```python
from wbsdk import WBClient
from wbsdk.exceptions import WBAuthError, WBRateLimitError

try:
    client = WBClient(token="...")
    result = client.content.get_parent_categories()
except WBAuthError:
    print("Неверный токен")
except WBRateLimitError:
    print("Превышен лимит запросов")
```

## Требования

- Python 3.10+
- httpx >= 0.27
- pydantic >= 2.0

## Лицензия

MIT
