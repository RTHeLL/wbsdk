"""Базовые Pydantic-схемы для WB API."""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ErrorDetail(BaseModel):
    """Детали ошибки API."""

    model_config = ConfigDict(extra="ignore")

    code: str | None = None
    message: str | None = None
    data: Any = None


class PaginationNext(BaseModel):
    """Параметр пагинации next."""

    model_config = ConfigDict(extra="ignore")

    next: int = Field(..., description="Значение для следующего запроса")


def validate_response(data: Any, model: type[BaseModel]) -> BaseModel:
    """Валидирует ответ через Pydantic-модель."""
    return model.model_validate(data)


def validate_list_response(data: Any, item_model: type[BaseModel]) -> list[BaseModel]:
    """Валидирует список через Pydantic-модель."""
    from pydantic import TypeAdapter

    adapter = TypeAdapter(list[item_model])
    return adapter.validate_python(data)
