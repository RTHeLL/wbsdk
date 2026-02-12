# WB SDK

[![PyPI version](https://img.shields.io/pypi/v/wbsdk)](https://pypi.org/project/wbsdk/)
[![Python versions](https://img.shields.io/pypi/pyversions/wbsdk.svg)](https://pypi.org/project/wbsdk/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/RTHeLL/wbsdk/actions/workflows/publish.yml/badge.svg)](https://github.com/RTHeLL/wbsdk/actions)

Python SDK для работы с [API Wildberries](https://dev.wildberries.ru/). Поддержка товаров, заказов, цен, складов, аналитики, рекламы, финансов и других разделов портала продавца.

---

## Возможности

| Модуль | Описание |
|--------|----------|
| **General** | Проверка подключения (ping), новости портала, информация о продавце |
| **Content** | Карточки товаров, категории, справочники, теги, медиафайлы |
| **Prices** | Цены, скидки, карантин, скидки WB Клуба, цены по размерам |
| **Marketplace (FBS)** | Заказы FBS, поставки, стикеры, пропуска, метаданные, история статусов |
| **Orders DBW** | Сборочные задания доставки курьером WB |
| **Orders DBS** | Сборочные задания витрины (DBS) |
| **Click Collect** | Заказы самовывоза |
| **Orders FBW** | Поставки на склад WB (приёмка, склады, транзитные тарифы) |
| **Warehouses** | Склады продавца (DBW), остатки, офисы, контакты |
| **Analytics** | Воронка продаж, поисковые запросы, остатки, отчёты (акцизы, приёмка, хранение, возвраты и др.), CSV-отчёты |
| **User Management** | Приглашения пользователей и управление доступом |
| **Tariffs** | Комиссии, тарифы на короба, паллеты, возврат, приёмку |
| **Communications** | Вопросы, отзывы, пины, чаты, претензии |
| **Reports** | Отчёты поставок, остатков, заказов, продаж (statistics-api) |
| **Promotion** | Реклама: кампании, ставки, бюджет, статистика; календарь акций |
| **Finances** | Баланс продавца |
| **Documents** | Категории и список документов, скачивание |
| **WBD** | Цифровые товары: ключи API, офферы, каталог |

**Встроенные механизмы:**

- **Синхронный и асинхронный клиенты** — `WBClient` и `AsyncWBClient`
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

Доступны **синхронный** (`WBClient`) и **асинхронный** (`AsyncWBClient`) клиенты. Все разделы API доступны через свойства клиента: `content`, `prices`, `marketplace`, `general`, `orders_dbw`, `orders_dbs`, `click_collect`, `orders_fbw`, `warehouses`, `analytics`, `promotion`, `promotion_calendar`, `communications`, `reports`, `finances`, `documents`, `tariffs`, `user_management`, `wbd`.

```python
from wbsdk import WBClient

client = WBClient(token="YOUR_API_TOKEN")

# Проверка подключения и новости
client.general.ping()  # PingResponse
# client.general.get_news(from_date="2024-01-01")

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

### Асинхронный клиент

Для неблокирующих запросов используйте `AsyncWBClient`.

```python
import asyncio
from wbsdk import AsyncWBClient

async def main():
    async with AsyncWBClient(token="YOUR_API_TOKEN") as client:
        categories = await client.content.get_parent_categories()
        orders = await client.marketplace.get_new_orders()
        # Те же методы, что у WBClient — с await
    # Клиент корректно закрыт (async with или await client.close())

asyncio.run(main())
```

Используйте `async with` или явный `await client.close()` после работы, чтобы закрыть HTTP-соединения.

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

### General — общий раздел

| Метод | Описание |
|-------|----------|
| `ping()` | Проверка подключения и валидности токена |
| `get_news()` | Новости портала продавцов |
| `get_seller_info()` | Информация о продавце |

### Marketplace — заказы FBS

| Метод | Описание |
|-------|----------|
| `get_new_orders()` | Новые сборочные задания |
| `get_orders()` | Заказы за период |
| `get_orders_status()` | Статусы сборочных заданий |
| `get_orders_status_history()` | История статусов (кроссбордер) |
| `get_orders_reshipment()` | Заказы, требующие переотправки |
| `cancel_order()` | Отмена заказа |
| `get_orders_stickers()`, `get_cross_border_stickers()` | Стикеры для заказов |
| `get_orders_metadata()`, `add_order_sgtin()`, `add_order_uin()` и др. | Метаданные заказов |
| `create_supply()`, `add_orders_to_supply()`, `deliver_supply()` | Поставки |
| `get_passes_offices()`, `get_passes()`, `create_pass()`, `update_pass()`, `delete_pass()` | Пропуска на склад |

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
| `get_search_report_table_groups()`, `get_search_report_table_details()` | Пагинация по поисковым отчётам |
| `get_search_report_product_search_texts()`, `get_search_report_product_orders()` | Поисковые запросы по товару |
| `get_stocks_groups()`, `get_stocks_products()` | Отчёты по остаткам |
| `get_stocks_report_offices()`, `get_stocks_report_products_sizes()` | Остатки по складам и размерам |
| `create_nm_report()`, `get_nm_report_file()` | CSV-отчёты |
| `get_excise_report()` | Отчёт по акцизам |
| `create_warehouse_remains_task()`, `get_warehouse_remains_task_download()` | Остатки на складе |
| `create_acceptance_report()`, `get_acceptance_report_task_download()` | Отчёт приёмки |
| `get_paid_storage()`, `get_paid_storage_task_download()` | Платное хранение |
| `get_region_sale()`, `get_brand_share()`, `get_banned_products_*()`, `get_goods_return()` | Продажи по регионам, доля бренда, заблокированные товары, возвраты |
| `get_measurement_penalties()`, `get_warehouse_measurements()`, `get_deductions()`, `get_antifraud_details()`, `get_goods_labeling()` | Штрафы, замеры, удержания, антифрод, маркировка |

### User Management — управление пользователями

| Метод | Описание |
|-------|----------|
| `create_invite()` | Создать приглашение |
| `get_users()` | Список пользователей |
| `update_users_access()` | Обновить доступ пользователей |

### Tariffs — тарифы

| Метод | Описание |
|-------|----------|
| `get_commission()` | Комиссия по категориям |
| `get_tariffs_box()`, `get_tariffs_pallet()`, `get_tariffs_return()` | Тарифы на короба, паллеты, возврат |
| `get_acceptance_coefficients()` | Коэффициенты приёмки по складам |

### Orders DBW — заказы доставки курьером WB

Доступ через `client.orders_dbw`. Новые и завершённые сборочные задания, статусы, даты доставки, отмена, метаданные (IMEI, УИН, GTIN, срок годности, ГТД и др.).

### Orders DBS — заказы витрины

Доступ через `client.orders_dbs`. Новые и завершённые заказы DBS, группы, клиенты, даты доставки, статусы, отмена, подтверждение, доставка, получение, метаданные.

### Click Collect — самовывоз

Доступ через `client.click_collect`. Новые заказы, подтверждение, готовность к выдаче, получение/отказ, проверка покупателя по коду.

### Orders FBW — поставки на склад WB

Доступ через `client.orders_fbw`. Коэффициенты приёмки, опции приёмки, склады WB, транзитные тарифы, список поставок FBW.

### Communications — вопросы, отзывы, чаты

Доступ через `client.communications`. Вопросы (количество, список, ответ), отзывы (количество, список, ответ, возврат), архив отзывов, пины, чаты, претензии.

### Reports — отчёты поставок и продаж

Доступ через `client.reports`. Поставки (`get_incomes`), остатки (`get_stocks`), заказы (`get_orders`), продажи (`get_sales`), отчёт по реализации (`get_report_detail_by_period`).

### Promotion — реклама и календарь акций

Доступ через `client.promotion` и `client.promotion_calendar`. Кампании (создание, запуск, пауза, ставки, бюджет, статистика), баланс рекламного счёта, нормзапросы, аукцион. Календарь: список акций, детали, номенклатуры, загрузка акций.

### Finances и Documents

Доступ через `client.finances` и `client.documents`. Баланс продавца (`get_balance`). Категории документов, список документов, скачивание одного или нескольких документов.

### WBD — цифровые товары

Доступ через `client.wbd`. Ключи API (список, погашенные), офферы (список, детали, ключи, цена, каталог), превью офферов.

---

## Обработка ошибок

Исключения одинаковы для синхронного и асинхронного клиента.

```python
from wbsdk import WBClient, AsyncWBClient
from wbsdk.exceptions import WBAuthError, WBRateLimitError, WBValidationError

# Синхронный клиент
try:
    with WBClient(token="...") as client:
        result = client.content.get_parent_categories()
except WBAuthError:
    print("Ошибка авторизации (401/403)")
except WBRateLimitError:
    print("Превышен лимит запросов (429)")
except WBValidationError:
    print("Ошибка валидации запроса (400/422)")

# Асинхронный клиент
async def fetch():
    try:
        async with AsyncWBClient(token="...") as client:
            return await client.content.get_parent_categories()
    except WBAuthError:
        print("Ошибка авторизации (401/403)")
```

---

## Документация WB

- [API Wildberries](https://dev.wildberries.ru/)
- [Песочница](https://dev.wildberries.ru/sandbox)
- [Общий раздел](https://dev.wildberries.ru/openapi/general) — ping, новости, информация о продавце
- [Работа с товарами](https://dev.wildberries.ru/openapi/work-with-products)
- [Заказы FBS](https://dev.wildberries.ru/openapi/orders-fbs)
- [Заказы DBW](https://dev.wildberries.ru/openapi/orders-dbw), [Заказы DBS](https://dev.wildberries.ru/openapi/orders-dbs), [Самовывоз](https://dev.wildberries.ru/openapi/in-store-pickup), [Поставки FBW](https://dev.wildberries.ru/openapi/orders-fbw)
- [Аналитика](https://dev.wildberries.ru/openapi/analytics)
- [Реклама](https://dev.wildberries.ru/openapi/promotion), [Вопросы и отзывы](https://dev.wildberries.ru/openapi/communications), [Отчёты](https://dev.wildberries.ru/openapi/reports), [Финансы](https://dev.wildberries.ru/openapi/finances), [WBD](https://dev.wildberries.ru/openapi/wbd)

---

## Лицензия

MIT License. См. [LICENSE](LICENSE).
