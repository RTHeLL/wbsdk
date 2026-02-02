"""Pydantic-схемы ответов Prices API."""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator


class PriceUploadResponse(BaseModel):
    """Ответ: загрузка цен/скидок."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    upload_id: int | None = Field(default=None, alias="uploadID")


class UploadStateResponse(BaseModel):
    """Ответ: статус выгрузки."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    data: list[dict[str, Any]] | dict[str, Any] | None = None
    upload_id: int | None = Field(default=None, alias="uploadID")


class UploadDetailsResponse(BaseModel):
    """Ответ: детали выгрузки."""

    model_config = ConfigDict(extra="ignore")

    data: list[dict[str, Any]] = Field(default_factory=list)
    total: int | None = None


class GoodsWithPrice(BaseModel):
    """Товар с ценой."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    nm_id: int | None = Field(default=None, alias="nmID")
    price: int | None = None
    discount: int | None = None
    promo_code: int | None = Field(default=None, alias="promoCode")


class GoodsWithPricesResponse(BaseModel):
    """Ответ: товары с ценами."""

    model_config = ConfigDict(extra="ignore")

    data: list[GoodsWithPrice] = Field(default_factory=list)
    total: int | None = None

    @model_validator(mode="before")
    @classmethod
    def _normalize_api_response(cls, value: Any) -> Any:
        if not isinstance(value, dict):
            return value
        data = value.get("data")
        if isinstance(data, dict) and "listGoods" in data:
            data = data["listGoods"]
        if data is None:
            data = []
        if "listGoods" in value and "data" not in value:
            data = value.get("listGoods") or []
        return {"data": data, "total": value.get("total")}


class GoodsSizeWithPrice(BaseModel):
    """Размер товара с ценой."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    chrt_id: int | None = Field(default=None, alias="chrtID")
    nm_id: int | None = Field(default=None, alias="nmID")
    price: int | None = None
    discount: int | None = None


class GoodsSizesResponse(BaseModel):
    """Ответ: цены по размерам товара."""

    model_config = ConfigDict(extra="ignore")

    data: list[GoodsSizeWithPrice] = Field(default_factory=list)
    total: int | None = None


class QuarantineGood(BaseModel):
    """Товар в карантине."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    nm_id: int | None = Field(default=None, alias="nmID")
    error: str | None = None


class QuarantineGoodsResponse(BaseModel):
    """Ответ: товары в карантине цен."""

    model_config = ConfigDict(extra="ignore")

    data: list[QuarantineGood] = Field(default_factory=list)
    total: int | None = None

    @model_validator(mode="before")
    @classmethod
    def _normalize_api_response(cls, value: Any) -> Any:
        if not isinstance(value, dict):
            return value
        data = value.get("data")
        if isinstance(data, dict) and "listGoods" in data:
            data = data["listGoods"]
        if data is None:
            data = []
        if "listGoods" in value and "data" not in value:
            data = value.get("listGoods") or []
        return {"data": data, "total": value.get("total")}
