# WB SDK

[![PyPI version](https://img.shields.io/pypi/v/wbsdk.svg)](https://pypi.org/project/wbsdk/)
[![Python versions](https://img.shields.io/pypi/pyversions/wbsdk.svg)](https://pypi.org/project/wbsdk/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/RTHeLL/wbsdk/actions/workflows/publish.yml/badge.svg)](https://github.com/RTHeLL/wbsdk/actions)

Python SDK для работы с [API Wildberries](https://dev.wildberries.ru/). Поддержка товаров, заказов, цен, складов и аналитики.

---

## Возможности

| Модуль | Описание |
|--------|----------|
| **Content** | Карточки товаров, категории, справочники, теги, медиафайлы |
| **Prices** | Цены, скидки, карантин, скидки WB Клуба, цены по размерам |
| **Marketplace (FBS)** | Заказы, поставки, стикеры, пропуска, метаданные заказов |
| **Warehouses** | Склады продавца (DBW), остатки, офисы, контакты |
| **Analytics** | Воронка продаж, поисковые запросы, отчёты по остаткам, CSV-отчёты |

**Встроенные механизмы:**

- Rate limiting по лимитам каждого API-домена WB
- Retry с exponential backoff при 429 (Too Many Requests)
- Типизированные исключения (401, 403, 422, 429 и др.)
- **Типизированные ответы** — методы возвращают Pydantic-объекты вместо словарей

---

## Установка

```bash
pip install wbsdk
```

Или из исходников:

```bash
git clone https://github.com/RTHeLL/wbsdk.git
cd wbsdk
pip install -e .
```

**Требования:** Python 3.10+

---

## Быстрый старт

```python
from wbsdk import WBClient

client = WBClient(token="YOUR_API_TOKEN")

# Категории и карточки (возвращаются Pydantic-объекты)
categories = client.content.get_parent_categories()  # ParentCategoriesResponse
cards = client.content.get_cards_list(settings={
    "cursor": {"limit": 100},
    "sort": {"ascending": True},
})

# Цены и скидки
client.prices.set_prices([{"nmID": 123, "price": 999, "discount": 30}])

# Заказы FBS
orders = client.marketplace.get_new_orders()  # OrdersNewResponse
supply = client.marketplace.create_supply(name="Поставка 1")  # SupplyCreateResponse
print(supply.id)  # доступ к полям через атрибуты (snake_case)

# Склады и остатки
warehouses = client.warehouses.get_warehouses()
client.warehouses.update_stocks(warehouse_id=1, stocks=[{"chrtId": 1, "sku": "123", "amount": 10}])

# Аналитика
funnel = client.analytics.get_sales_funnel_products(
    selected_period={"start": "2024-01-01", "end": "2024-01-31"},
)
```

### Песочница

Для тестирования на случайных данных используйте [песочницу WB](https://dev.wildberries.ru/sandbox). Нужен токен с опцией **«Тестовый контур»** в личном кабинете WB.

```python
client = WBClient(token="YOUR_SANDBOX_TOKEN", sandbox=True)
# Дальше вызовы идут на sandbox-хосты (content-api-sandbox, marketplace-api-sandbox и т.д.)
categories = client.content.get_parent_categories()
```

В песочнице действуют свои лимиты (например, 1 запрос в секунду для многих разделов).

---

## Типизированные ответы

Методы API возвращают **Pydantic-объекты**, а не сырые словари или списки. Все поля — в snake_case.

```python
# Доступ к данным через атрибуты
categories = client.content.get_parent_categories()
for cat in categories.data:
    print(cat.name, cat.parent_id)

orders = client.marketplace.get_new_orders()
for order in orders.orders:
    print(order.id, order.nm_id, order.price)

supply = client.marketplace.create_supply(name="Тест")
print(supply.id)  # WB-GI-1234567

tags = client.content.get_tags()
for tag in tags.data:
    print(tag.id, tag.name, tag.color)
```

Схемы доступны в `wbsdk.schemas` для аннотаций и кастомной логики.

---

## API по модулям

### Content — контент и карточки

| Метод | Описание |
|-------|----------|
| `get_parent_categories()` | Родительские категории |
| `get_subjects()` | Подкатегории (предметы) |
| `get_subject_characteristics()` | Характеристики предмета |
| `get_colors()`, `get_countries()`, `get_vat_rates()` | Справочники |
| `create_cards()`, `update_cards()` | Создание и обновление карточек |
| `get_cards_list()`, `get_cards_trash_list()` | Список карточек и корзина |
| `generate_barcodes()` | Генерация штрихкодов |
| `get_tags()`, `create_tag()`, `link_tags_to_card()` | Теги |
| `upload_media_file()`, `upload_media_by_links()` | Загрузка медиа |

### Prices — цены и скидки

| Метод | Описание |
|-------|----------|
| `set_prices()` | Установка цен и скидок (до 1000 шт.) |
| `set_size_prices()` | Цены по размерам |
| `set_club_discounts()` | Скидки WB Клуба |
| `get_goods_with_prices()` | Товары с ценами |
| `get_quarantine_goods()` | Товары в карантине цен |
| `get_processed_upload_state()` | Статус выгрузки цен |

### Marketplace — заказы FBS

| Метод | Описание |
|-------|----------|
| `get_new_orders()` | Новые сборочные задания |
| `get_orders()` | Заказы за период |
| `cancel_order()` | Отмена заказа |
| `get_orders_stickers()` | Стикеры для заказов |
| `create_supply()` | Создание поставки |
| `add_orders_to_supply()` | Добавление заказов в поставку |
| `get_passes_offices()`, `create_pass()` | Пропуска на склад |

### Warehouses — склады

| Метод | Описание |
|-------|----------|
| `get_offices()` | Офисы для привязки |
| `get_warehouses()` | Список складов |
| `create_warehouse()` | Создание склада |
| `get_stocks()`, `update_stocks()` | Остатки |

### Analytics — аналитика

| Метод | Описание |
|-------|----------|
| `get_sales_funnel_products()` | Воронка по карточкам |
| `get_sales_funnel_products_history()` | История по дням |
| `get_search_report()` | Отчёт по поисковым запросам |
| `get_stocks_groups()`, `get_stocks_products()` | Отчёты по остаткам |
| `create_nm_report()`, `get_nm_report_file()` | CSV-отчёты |

---

## Обработка ошибок

```python
from wbsdk import WBClient
from wbsdk.exceptions import WBAuthError, WBRateLimitError, WBValidationError

try:
    client = WBClient(token="...")
    result = client.content.get_parent_categories()
except WBAuthError:
    print("Ошибка авторизации (401/403)")
except WBRateLimitError:
    print("Превышен лимит запросов (429)")
except WBValidationError:
    print("Ошибка валидации запроса (400/422)")
```

---

## Документация WB

- [API Wildberries](https://dev.wildberries.ru/)
- [Песочница](https://dev.wildberries.ru/sandbox)
- [Работа с товарами](https://dev.wildberries.ru/openapi/work-with-products)
- [Заказы FBS](https://dev.wildberries.ru/openapi/orders-fbs)
- [Аналитика](https://dev.wildberries.ru/openapi/analytics)

---

## Лицензия

MIT License. См. [LICENSE](LICENSE).
