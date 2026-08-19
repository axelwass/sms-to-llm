from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

security = HTTPBearer(auto_error=False)


class AuthorizationService:
    """Bearer-token authorization with user/admin role checks."""

    def __init__(
        self,
        admins: list[str] | None = None,
        users: list[str] | None = None,
    ) -> None:
        self.admins = admins or ["admin"]
        self.users = users or ["admin", "user"]

    def is_authorized(self, token: str) -> bool:
        return token in self.users

    def is_admin(self, token: str) -> bool:
        return token in self.admins

    def ensure_user(self, credentials: HTTPAuthorizationCredentials | None) -> None:
        if credentials is None or not self.is_authorized(credentials.credentials):
            raise HTTPException(status_code=401, detail="Unauthorized")

    def ensure_admin(self, credentials: HTTPAuthorizationCredentials | None) -> None:
        self.ensure_user(credentials)
        if credentials is None or not self.is_admin(credentials.credentials):
            raise HTTPException(status_code=403, detail="Forbidden")


authorization_service = AuthorizationService()


async def require_user_key(
    credentials: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(security),
    ],
) -> None:
    authorization_service.ensure_user(credentials)


async def require_admin_key(
    credentials: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(security),
    ],
) -> None:
    authorization_service.ensure_admin(credentials)
