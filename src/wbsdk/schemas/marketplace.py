"""Pydantic-схемы ответов Marketplace API."""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class OrderNew(BaseModel):
    """Новый заказ (краткая структура)."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    id: int | None = None
    rid: str | None = None
    created_at: str | None = Field(default=None, alias="createdAt")
    warehouse_id: int | None = Field(default=None, alias="warehouseId")
    nm_id: int | None = Field(default=None, alias="nmId")
    chrt_id: int | None = Field(default=None, alias="chrtId")
    article: str | None = None
    skus: list[str] = Field(default_factory=list)
    price: int | None = None
    converted_price: int | None = Field(default=None, alias="convertedPrice")
    currency_code: int | None = Field(default=None, alias="currencyCode")
    converted_currency_code: int | None = Field(default=None, alias="convertedCurrencyCode")
    cargo_type: int | None = Field(default=None, alias="cargoType")
    delivery_type: str | None = Field(default=None, alias="deliveryType")
    order_uid: str | None = Field(default=None, alias="orderUid")
    address: dict[str, Any] | None = None
    comment: str | None = None
    is_zero_order: bool | None = Field(default=None, alias="isZeroOrder")


class OrdersNewResponse(BaseModel):
    """Ответ: новые заказы."""

    model_config = ConfigDict(extra="ignore")

    orders: list[OrderNew] = Field(default_factory=list)


class Order(BaseModel):
    """Заказ (полная структура)."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    id: int | None = None
    rid: str | None = None
    created_at: str | None = Field(default=None, alias="createdAt")
    warehouse_id: int | None = Field(default=None, alias="warehouseId")
    nm_id: int | None = Field(default=None, alias="nmId")
    chrt_id: int | None = Field(default=None, alias="chrtId")
    article: str | None = None
    skus: list[str] = Field(default_factory=list)
    price: int | None = None
    converted_price: int | None = Field(default=None, alias="convertedPrice")
    currency_code: int | None = Field(default=None, alias="currencyCode")
    converted_currency_code: int | None = Field(default=None, alias="convertedCurrencyCode")
    cargo_type: int | None = Field(default=None, alias="cargoType")
    delivery_type: str | None = Field(default=None, alias="deliveryType")
    order_uid: str | None = Field(default=None, alias="orderUid")
    address: dict[str, Any] | None = None
    comment: str | None = None


class OrdersResponse(BaseModel):
    """Ответ: список заказов с пагинацией."""

    model_config = ConfigDict(extra="ignore")

    next: int = 0
    orders: list[Order] = Field(default_factory=list)


class OrderStatus(BaseModel):
    """Статус заказа."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    id: int = 0
    supplier_status: str = Field(default="", alias="supplierStatus")
    wb_status: str = Field(default="", alias="wbStatus")


class OrdersStatusResponse(BaseModel):
    """Ответ: статусы заказов."""

    model_config = ConfigDict(extra="ignore")

    orders: list[OrderStatus] = Field(default_factory=list)


class ReshipmentOrder(BaseModel):
    """Заказ на переотправку."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    supply_id: str | None = Field(default=None, alias="supplyID")
    order_id: int | None = Field(default=None, alias="orderID")


class ReshipmentResponse(BaseModel):
    """Ответ: заказы на переотправку."""

    model_config = ConfigDict(extra="ignore")

    orders: list[ReshipmentOrder] = Field(default_factory=list)


class OrderSticker(BaseModel):
    """Стикер заказа."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    order_id: int = Field(default=0, alias="orderId")
    part_a: int = Field(default=0, alias="partA")
    part_b: int = Field(default=0, alias="partB")
    barcode: str = ""
    file: str = ""


class StickersResponse(BaseModel):
    """Ответ: стикеры заказов."""

    model_config = ConfigDict(extra="ignore")

    stickers: list[OrderSticker] = Field(default_factory=list)


class CrossBorderSticker(BaseModel):
    """Стикер кросс-бордер заказа."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    order_id: int = Field(default=0, alias="orderID")
    url: str = ""
    parcel_id: str = Field(default="", alias="parcelID")


class CrossBorderStickersResponse(BaseModel):
    """Ответ: стикеры кросс-бордер заказов."""

    model_config = ConfigDict(extra="ignore")

    stickers: list[CrossBorderSticker] = Field(default_factory=list)


class OrderMeta(BaseModel):
    """Метаданные заказа."""

    model_config = ConfigDict(extra="ignore")

    imei: list[str] = Field(default_factory=list)
    uin: list[str] = Field(default_factory=list)
    gtin: list[str] = Field(default_factory=list)
    sgtin: list[str] = Field(default_factory=list)


class OrderMetaResponse(BaseModel):
    """Ответ: метаданные заказов."""

    model_config = ConfigDict(extra="ignore")

    meta: OrderMeta | list[OrderMeta] | None = None


class SupplyCreateResponse(BaseModel):
    """Ответ: создание поставки."""

    model_config = ConfigDict(extra="ignore")

    id: str = ""


class Supply(BaseModel):
    """Поставка."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    id: str = ""
    done: bool | None = None
    created_at: str | None = Field(default=None, alias="createdAt")
    closed_at: str | None = Field(default=None, alias="closedAt")
    cargo_type: int | None = Field(default=None, alias="cargoType")


class SuppliesResponse(BaseModel):
    """Ответ: список поставок."""

    model_config = ConfigDict(extra="ignore")

    next: int = 0
    supplies: list[Supply] = Field(default_factory=list)


class SupplyOrder(BaseModel):
    """Заказ в поставке."""

    model_config = ConfigDict(extra="ignore")

    id: int | None = None


class SupplyOrderIdsResponse(BaseModel):
    """Ответ: ID заказов в поставке."""

    model_config = ConfigDict(extra="ignore")

    orders: list[int] = Field(default_factory=list)


class BarcodeResponse(BaseModel):
    """Ответ: QR-код поставки."""

    model_config = ConfigDict(extra="ignore")

    barcode: str = ""
    file: str = ""


class SupplyTrbx(BaseModel):
    """Коробка поставки."""

    model_config = ConfigDict(extra="ignore")

    id: str | None = None
    orders: list[int] = Field(default_factory=list)


class SupplyBoxesResponse(BaseModel):
    """Ответ: список коробок поставки."""

    model_config = ConfigDict(extra="ignore")

    trbxes: list[SupplyTrbx] = Field(default_factory=list)


class TrbxIdsResponse(BaseModel):
    """Ответ: ID созданных коробок."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    trbx_ids: list[str] = Field(default_factory=list, alias="trbxIds")


class TrbxSticker(BaseModel):
    """Стикер коробки."""

    model_config = ConfigDict(extra="ignore")

    id: str | None = None
    file: str = ""


class TrbxStickersResponse(BaseModel):
    """Ответ: стикеры коробок."""

    model_config = ConfigDict(extra="ignore")

    stickers: list[TrbxSticker] = Field(default_factory=list)


class PassOffice(BaseModel):
    """Офис для пропуска."""

    model_config = ConfigDict(extra="ignore")

    id: int = 0
    name: str = ""
    address: str = ""


class Pass(BaseModel):
    """Пропуск."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    id: int = 0
    first_name: str | None = Field(default=None, alias="firstName")
    last_name: str | None = Field(default=None, alias="lastName")
    car_model: str | None = Field(default=None, alias="carModel")
    car_number: str | None = Field(default=None, alias="carNumber")
    office_id: int | None = Field(default=None, alias="officeId")


class PassCreateResponse(BaseModel):
    """Ответ: создание пропуска."""

    model_config = ConfigDict(extra="ignore")

    id: int = 0


class OrdersClientInfoResponse(BaseModel):
    """Ответ: информация о клиенте по заказам (кросс-бордер)."""

    model_config = ConfigDict(extra="ignore")

    orders: list[dict[str, Any]] = Field(default_factory=list)
