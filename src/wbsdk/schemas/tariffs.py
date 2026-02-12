"""Pydantic-схемы Tariffs API (common-api)."""

from typing import Any

from pydantic import BaseModel, ConfigDict


class TariffsResponse(BaseModel):
    """Ответ с данными тарифов (произвольная структура)."""

    model_config = ConfigDict(extra="ignore")

    data: Any = None
    report: Any = None
