"""Pydantic-схемы ответов Warehouses API."""

from pydantic import BaseModel, ConfigDict, Field


class Office(BaseModel):
    """Офис для привязки к складу."""

    model_config = ConfigDict(extra="ignore")

    id: int = 0
    name: str = ""
    address: str = ""


class Warehouse(BaseModel):
    """Склад продавца."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    id: int = 0
    name: str = ""
    office_id: int | None = Field(default=None, alias="officeId")


class WarehouseCreateResponse(BaseModel):
    """Ответ: создание склада."""

    model_config = ConfigDict(extra="ignore")

    id: int = 0


class StoreContact(BaseModel):
    """Контакт склада (DBW)."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    contact_type: str | None = Field(default=None, alias="contactType")
    contact: str | None = None


class StockItem(BaseModel):
    """Элемент остатка."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    sku: str = ""
    amount: int = 0
    chrt_id: int | None = Field(default=None, alias="chrtId")


class StocksResponse(BaseModel):
    """Ответ: остатки склада."""

    model_config = ConfigDict(extra="ignore")

    stocks: list[StockItem] = Field(default_factory=list)
