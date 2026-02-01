"""Pydantic-схемы ответов Analytics API."""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class SalesFunnelProductsResponse(BaseModel):
    """Ответ: воронка продаж по карточкам."""

    model_config = ConfigDict(extra="ignore")

    data: Any = None
    total: int | None = None
    cursor: dict[str, Any] | None = None


class SalesFunnelHistoryResponse(BaseModel):
    """Ответ: история воронки продаж."""

    model_config = ConfigDict(extra="ignore")

    data: Any = None


class SalesFunnelGroupedResponse(BaseModel):
    """Ответ: сгруппированная история воронки."""

    model_config = ConfigDict(extra="ignore")

    data: Any = None


class SearchReportResponse(BaseModel):
    """Ответ: отчёт по поисковым запросам."""

    model_config = ConfigDict(extra="ignore")

    data: Any = None
    total: int | None = None
    cursor: dict[str, Any] | None = None


class StocksGroupsResponse(BaseModel):
    """Ответ: остатки по группам."""

    model_config = ConfigDict(extra="ignore")

    data: Any = None
    total: int | None = None
    cursor: dict[str, Any] | None = None


class StocksProductsResponse(BaseModel):
    """Ответ: остатки по товарам."""

    model_config = ConfigDict(extra="ignore")

    data: Any = None
    total: int | None = None
    cursor: dict[str, Any] | None = None


class NmReportCreateResponse(BaseModel):
    """Ответ: создание NM-отчёта."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    data: dict[str, Any] | None = None
    download_id: str | None = Field(default=None, alias="downloadID")


class NmReportItem(BaseModel):
    """Элемент списка NM-отчётов."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    download_id: str | None = Field(default=None, alias="downloadID")
    report_type: str | None = Field(default=None, alias="reportType")
    status: str | None = None
    created_at: str | None = Field(default=None, alias="createdAt")
    updated_at: str | None = Field(default=None, alias="updatedAt")


class NmReportsListResponse(BaseModel):
    """Ответ: список NM-отчётов."""

    model_config = ConfigDict(extra="ignore")

    data: list[NmReportItem] | list[dict[str, Any]] = Field(default_factory=list)


class NmReportRetryResponse(BaseModel):
    """Ответ: повторная генерация NM-отчёта."""

    model_config = ConfigDict(extra="ignore")

    data: dict[str, Any] | None = None
    error: bool = False
