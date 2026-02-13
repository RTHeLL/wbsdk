"""Pydantic-схемы ответов Content API."""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ParentCategory(BaseModel):
    """Родительская категория."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    id: int | None = None
    name: str | None = None
    parent_id: int | None = Field(default=None, alias="parentID")
    parent_name: str | None = Field(default=None, alias="parentName")
    is_visible: bool | None = Field(default=None, alias="isVisible")


class ParentCategoriesResponse(BaseModel):
    """Ответ: родительские категории."""

    model_config = ConfigDict(extra="ignore")

    data: list[ParentCategory] = Field(default_factory=list)
    error: bool = False


class Subject(BaseModel):
    """Предмет (подкатегория)."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    subject_id: int | None = Field(default=None, alias="subjectID")
    subject_name: str | None = Field(default=None, alias="subjectName")
    parent_id: int | None = Field(default=None, alias="parentID")
    parent_name: str | None = Field(default=None, alias="parentName")


class SubjectsResponse(BaseModel):
    """Ответ: список предметов."""

    model_config = ConfigDict(extra="ignore")

    data: list[Subject] = Field(default_factory=list)
    error: bool = False


class SubjectCharacteristic(BaseModel):
    """Характеристика предмета."""

    model_config = ConfigDict(extra="ignore")

    id: int | None = None
    name: str | None = None
    required: bool | None = None
    unit: str | None = None
    values: list[Any] = Field(default_factory=list)


class SubjectCharacteristicsResponse(BaseModel):
    """Ответ: характеристики предмета."""

    model_config = ConfigDict(extra="ignore")

    data: list[SubjectCharacteristic] | list[dict[str, Any]] = Field(default_factory=list)
    error: bool = False


class DirectoryItem(BaseModel):
    """Элемент справочника."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    id: int | str | None = None
    name: str | None = None
    hex_code: str | None = Field(default=None, alias="hexCode")
    parent_id: int | None = Field(default=None, alias="parentID")


class DirectoryListResponse(BaseModel):
    """Ответ со списком элементов справочника.

    API возвращает {\"data\": [...]}, иногда data — массив строк (kinds).
    """

    model_config = ConfigDict(extra="ignore")

    data: list[DirectoryItem] = Field(default_factory=list)

    @model_validator(mode="before")
    @classmethod
    def _normalize_api_response(cls, value: Any) -> Any:
        if value is None:
            return {"data": []}
        if isinstance(value, list):
            value = {"data": value}
        if isinstance(value, dict) and "data" in value:
            data = value["data"]
            if isinstance(data, list):
                value = {
                    **value,
                    "data": [{"name": x} if isinstance(x, str) else x for x in data],
                }
        return value


class TnvedResponse(BaseModel):
    """Ответ: коды ТН ВЭД."""

    model_config = ConfigDict(extra="ignore")

    data: list[dict[str, Any]] = Field(default_factory=list)
    error: bool = False


class Brand(BaseModel):
    """Бренд."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    id: int | None = None
    name: str | None = None
    brand_name: str | None = Field(default=None, alias="brandName")


class BrandsResponse(BaseModel):
    """Ответ: список брендов."""

    model_config = ConfigDict(extra="ignore")

    data: list[Brand] | list[dict[str, Any]] = Field(default_factory=list)
    next: int | None = None
    error: bool = False


class CardsLimitsResponse(BaseModel):
    """Ответ: лимиты карточек."""

    model_config = ConfigDict(extra="ignore")

    data: dict[str, Any] | None = None
    error: bool = False


class BarcodesResponse(BaseModel):
    """Ответ: генерация штрихкодов."""

    model_config = ConfigDict(extra="ignore")

    data: list[str] = Field(default_factory=list)
    error: bool = False


class ContentMutationResponse(BaseModel):
    """Ответ: создание/обновление контента."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    data: dict[str, Any] | list[Any] | None = None
    error: bool = False
    upload_id: int | None = Field(default=None, alias="uploadID")
    added: list[dict[str, Any]] = Field(default_factory=list)
    rejected: list[dict[str, Any]] = Field(default_factory=list)


class CardsListResponse(BaseModel):
    """Ответ: список карточек."""

    model_config = ConfigDict(extra="ignore")

    data: dict[str, Any] | list[dict[str, Any]] | None = None
    cursor: dict[str, Any] | None = None
    error: bool = False


class Tag(BaseModel):
    """Тег."""

    model_config = ConfigDict(extra="ignore")

    id: int = 0
    name: str = ""
    color: str = ""


class TagsResponse(BaseModel):
    """Ответ: список тегов."""

    model_config = ConfigDict(extra="ignore")

    data: list[Tag] = Field(default_factory=list)
    error: bool = False


class TagMutationResponse(BaseModel):
    """Ответ: создание/обновление тега."""

    model_config = ConfigDict(extra="ignore")

    data: dict[str, Any] | Tag | None = None
    error: bool = False
