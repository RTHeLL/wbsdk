"""
Примеры использования WB SDK (WBClient и AsyncWBClient).

Перед запуском установите переменную окружения WB_TOKEN с вашим API-токеном.
"""

import asyncio
import os

from wbsdk import AsyncWBClient, WBClient

# Токен можно передать напрямую или получить из переменной окружения
token = os.environ.get("WB_TOKEN", "YOUR_TOKEN_HERE")


def example_content() -> None:
    """Пример работы с контентом."""
    with WBClient(token=token) as client:
        # Категории
        categories = client.content.get_parent_categories()
        print("Категории:", categories)

        # Список карточек
        cards = client.content.get_cards_list(
            settings={
                "cursor": {"limit": 10},
                "sort": {"ascending": True},
            }
        )
        print("Карточки:", cards)


def example_prices() -> None:
    """Пример работы с ценами."""
    with WBClient(token=token) as client:
        # Установка цен
        result = client.prices.set_prices([
            {"nmID": 123, "price": 999, "discount": 30},
        ])
        print("Результат установки цен:", result)


def example_marketplace() -> None:
    """Пример работы с заказами FBS."""
    with WBClient(token=token) as client:
        # Новые заказы
        orders = client.marketplace.get_new_orders()
        print("Новые заказы:", orders)

        # Создание поставки
        supply = client.marketplace.create_supply(name="Моя поставка")
        print("Создана поставка:", supply)


def example_warehouses() -> None:
    """Пример работы со складами."""
    with WBClient(token=token) as client:
        offices = client.warehouses.get_offices()
        warehouses = client.warehouses.get_warehouses()
        print("Офисы:", offices)
        print("Склады:", warehouses)


async def example_async_content() -> None:
    """Асинхронный пример."""
    async with AsyncWBClient(token=token) as client:
        categories = await client.content.get_parent_categories()
        print("Категории (async):", categories)


if __name__ == "__main__":
    print("Примеры WB SDK. Замените token на свой для тестирования.")
    # example_content()
    # asyncio.run(example_async_content())
