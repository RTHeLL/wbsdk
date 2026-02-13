"""Pydantic-схемы General API (common-api)."""


from pydantic import BaseModel, ConfigDict, Field


class PingResponse(BaseModel):
    """Ответ проверки подключения."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    ts: str | None = Field(default=None, alias="TS")
    status: str | None = Field(default=None, alias="Status")


class NewsType(BaseModel):
    """Тег новости."""

    model_config = ConfigDict(extra="ignore")

    id: int = 0
    name: str = ""


class NewsItem(BaseModel):
    """Элемент новости портала."""

    model_config = ConfigDict(extra="ignore")

    id: int = 0
    header: str = ""
    content: str = ""
    date: str = ""
    types: list[NewsType] = Field(default_factory=list)


class NewsResponse(BaseModel):
    """Ответ: новости портала продавцов."""

    model_config = ConfigDict(extra="ignore")

    data: list[NewsItem] = Field(default_factory=list)


class SellerInfoResponse(BaseModel):
    """Ответ: информация о продавце."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str = ""
    sid: str = ""
    trade_mark: str = Field(default="", alias="tradeMark")
