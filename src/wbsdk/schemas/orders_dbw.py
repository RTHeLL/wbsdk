"""Pydantic-схемы Orders DBW API."""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class OrdersListResponse(BaseModel):
    """Ответ: список заказов DBW с пагинацией."""

    model_config = ConfigDict(extra="ignore")

    next: int = 0
    orders: list[dict[str, Any]] = Field(default_factory=list)


class OrdersNewResponse(BaseModel):
    """Ответ: новые заказы DBW."""

    model_config = ConfigDict(extra="ignore")

    orders: list[dict[str, Any]] = Field(default_factory=list)
