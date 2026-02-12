"""Pydantic-схемы User Management API."""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class AccessItem(BaseModel):
    """Доступ к разделу профиля."""

    model_config = ConfigDict(extra="ignore")

    code: str = ""
    disabled: bool = False


class InviteeInfo(BaseModel):
    """Информация о приглашении."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    phone_number: str = Field(default="", alias="phoneNumber")
    position: str = ""
    invite_uuid: str = Field(default="", alias="inviteUuid")
    expired_at: str = Field(default="", alias="expiredAt")
    is_active: bool = Field(default=False, alias="isActive")


class User(BaseModel):
    """Пользователь продавца."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    id: int = 0
    role: str = ""
    position: str = ""
    phone: str = ""
    email: str = ""
    is_owner: bool = Field(default=False, alias="isOwner")
    first_name: str = Field(default="", alias="firstName")
    second_name: str = Field(default="", alias="secondName")
    patronymic: str = ""
    goods_return: bool = Field(default=False, alias="goodsReturn")
    is_invitee: bool = Field(default=False, alias="isInvitee")
    invitee_info: InviteeInfo | None = Field(default=None, alias="inviteeInfo")
    access: list[AccessItem] = Field(default_factory=list)


class GetUsersResponse(BaseModel):
    """Ответ: список пользователей."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    total: int = 0
    count_in_response: int = Field(default=0, alias="countInResponse")
    users: list[User] = Field(default_factory=list)


class CreateInviteResponse(BaseModel):
    """Ответ: создание приглашения."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    invite_id: str = Field(default="", alias="inviteID")
    expired_at: str = Field(default="", alias="expiredAt")
    is_success: bool = Field(default=False, alias="isSuccess")
    invite_url: str = Field(default="", alias="inviteUrl")
