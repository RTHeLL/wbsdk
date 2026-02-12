"""Pydantic-схемы Click&Collect (самовывоз) API."""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class OrdersNewResponse(BaseModel):
    """Ответ: новые заказы самовывоза."""

    model_config = ConfigDict(extra="ignore")

    orders: list[dict[str, Any]] = Field(default_factory=list)


class OrdersListResponse(BaseModel):
    """Ответ: список заказов самовывоза с пагинацией."""

    model_config = ConfigDict(extra="ignore")

    next: int = 0
    orders: list[dict[str, Any]] = Field(default_factory=list)
