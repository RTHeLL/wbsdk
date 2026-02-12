"""API управления пользователями продавца (user-management-api)."""

from typing import Any

from wbsdk.api.base import BaseAPI
from wbsdk.schemas.user_management import (
    CreateInviteResponse,
    GetUsersResponse,
)


class UserManagementAPI(BaseAPI):
    """API приглашений и доступа пользователей."""

    def __init__(self, client: Any, base_url: str):
        super().__init__(client, base_url, domain="user_management")

    def create_invite(
        self,
        phone_number: str,
        *,
        position: str | None = None,
        access: list[dict[str, Any]] | None = None,
    ) -> CreateInviteResponse:
        """Создать приглашение для нового пользователя."""
        payload: dict[str, Any] = {
            "invite": {"phoneNumber": phone_number},
        }
        if position is not None:
            payload["invite"]["position"] = position
        if access is not None:
            payload["access"] = access
        return self.post(
            "/api/v1/invite",
            json=payload,
            response_model=CreateInviteResponse,
        )

    def get_users(
        self,
        *,
        limit: int = 100,
        offset: int = 0,
        is_invite_only: bool = False,
    ) -> GetUsersResponse:
        """Список активных или приглашённых пользователей."""
        params: dict[str, Any] = {
            "limit": limit,
            "offset": offset,
            "isInviteOnly": is_invite_only,
        }
        return self.get(
            "/api/v1/users",
            params=params,
            response_model=GetUsersResponse,
        )

    def update_users_access(
        self,
        users_accesses: list[dict[str, Any]],
    ) -> None:
        """Изменить права доступа пользователям."""
        self.put(
            "/api/v1/users/access",
            json={"usersAccesses": users_accesses},
        )

    def delete_user(self, user_id: int) -> None:
        """Удалить пользователя из списка сотрудников."""
        self.delete(
            "/api/v1/user",
            params={"deletedUserID": user_id},
        )
